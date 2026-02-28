import type { ChatMessage, SendMessageRequest } from '~/types/chat'
import { useAutoScroll } from './useAutoScroll'
import { useModelSelection } from './useModelSelection'
import { readonly, ref, watch } from 'vue'

export const useChat = () => {
  // 模型選擇
  const { selectedModel } = useModelSelection()
  // 狀態管理
  const messages = ref<ChatMessage[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const chatContainerRef = ref<HTMLElement | null>(null)

  // 打字效果
  const typingEffect = useTypingEffect(40) // 40ms 間隔

  // API 基礎 URL
  const API_BASE_URL = 'http://localhost:8000'

  // 當前正在打字的 AI 訊息索引
  const currentTypingIndex = ref<number | null>(null)

  // 初始化自動滾動
  const autoScrollHelper = useAutoScroll(chatContainerRef)
  autoScrollHelper.init()

  /**
   * 同步 typedText 到 messages（手動呼叫，確保最終狀態）
   */
  const syncTypedTextToMessage = () => {
    if (currentTypingIndex.value !== null && currentTypingIndex.value < messages.value.length) {
      const finalIndex = currentTypingIndex.value
      messages.value[finalIndex] = {
        ...messages.value[finalIndex],
        content: typingEffect.typedText.value
      }
    }
  }

  /**
   * 監聽 typedText 變化，同步更新 AI 訊息內容
   */
  watch(typingEffect.typedText, (newText) => {
    if (currentTypingIndex.value !== null && currentTypingIndex.value < messages.value.length) {
      const currentMessage = messages.value[currentTypingIndex.value]
      messages.value[currentTypingIndex.value] = {
        ...currentMessage,
        content: newText
      }
      autoScrollHelper.debouncedAutoScroll()
    }
  })

  /**
   * 發送訊息並接收 SSE streaming 回應
   */
  const sendMessage = async (message: string) => {
    if (!message.trim()) return

    // 清除錯誤
    error.value = null
    isLoading.value = true

    // 添加使用者訊息
    const userMessage: ChatMessage = {
      role: 'user',
      content: message.trim(),
      timestamp: new Date()
    }
    messages.value.push(userMessage)
    autoScrollHelper.smoothScrollToBottom()

    // 準備 AI 訊息佔位
    const aiMessage: ChatMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date()
    }
    messages.value.push(aiMessage)
    const aiMessageIndex = messages.value.length - 1

    // 設定當前打字索引並重置打字效果
    currentTypingIndex.value = aiMessageIndex
    typingEffect.reset()

    try {
      // 發送 POST 請求
      const response = await fetch(`${API_BASE_URL}/api/chat/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          model: selectedModel.value
        } as SendMessageRequest),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // 確保回應是 ReadableStream
      if (!response.body) {
        throw new Error('No response body')
      }

      // 讀取 SSE stream
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let typingStarted = false
      let streamDone = false

      while (true) {
        const { done, value } = await reader.read()

        if (done) {
          // Stream 結束，flush TextDecoder 中的殘留多字節字符
          buffer += decoder.decode()
          streamDone = true
        } else {
          // 解碼 chunk（使用 stream 模式以正確處理多字節字符）
          buffer += decoder.decode(value, { stream: true })
        }

        const events = buffer.split('\n\n')

        // 保留最後一個未完成的事件
        buffer = events.pop() || ''

        for (const event of events) {
          const lines = event.split('\n').filter(line => line.trim())

          let eventType = ''
          let eventData = ''

          for (const line of lines) {
            if (line.startsWith('event: ')) {
              eventType = line.slice(7).trim()
            } else if (line.startsWith('data: ')) {
              eventData = line.slice(6).trim()
            }
          }

          // 處理各類型事件
          if (eventType === 'start') {
            // 準備開始接收，但等第一個 chunk 才啟動打字
          } else if (eventType === 'chunk' && eventData) {
            try {
              const parsed = JSON.parse(eventData)
              if (parsed.content) {
                // 第一個 chunk 時啟動打字效果
                if (!typingStarted) {
                  typingEffect.startTyping()
                  typingStarted = true
                }
                // 將字符加入隊列
                typingEffect.enqueueCharacters(parsed.content)
              }
            } catch (e) {
              console.error('解析 chunk 失敗:', e)
            }
          } else if (eventType === 'done') {
            // 停止打字效果，立即渲染剩餘字符
            typingEffect.stopTyping()

            // 關鍵修復：在清空 index 之前，手動同步最終內容
            // 因為 watch 是異步的，可能在 currentTypingIndex 被清空後才執行
            syncTypedTextToMessage()

            // 強制滾到底部確保看到完整內容
            await autoScrollHelper.smoothScrollToBottom()

            isLoading.value = false
            currentTypingIndex.value = null
            // 不使用 break，改用 flag 標記，確保所有事件處理完成
            streamDone = true
          } else if (eventType === 'error' && eventData) {
            try {
              const errorObj = JSON.parse(eventData)
              throw new Error(errorObj.error || '未知錯誤')
            } catch (e) {
              throw new Error(eventData)
            }
          }
        }

        // 如果 stream 已結束且已處理 done 事件，退出迴圈
        if (streamDone) break
      }

    } catch (err) {
      console.error('發送訊息錯誤:', err)
      error.value = err instanceof Error ? err.message : '發送訊息失敗'

      // 停止打字效果
      typingEffect.stopTyping()
      currentTypingIndex.value = null

      // 移除失敗的 AI 訊息
      messages.value.pop()
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 清除對話歷史
   */
  const clearHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/clear`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error('清除歷史失敗')
      }

      // 清空本地訊息
      messages.value = []
      error.value = null
      typingEffect.reset()
      currentTypingIndex.value = null
    } catch (err) {
      console.error('清除歷史錯誤:', err)
      error.value = err instanceof Error ? err.message : '清除歷史失敗'
    }
  }

  return {
    messages: readonly(messages),
    isLoading: readonly(isLoading),
    isTyping: typingEffect.isTyping,
    isAtBottom: autoScrollHelper.isAtBottom,
    error: readonly(error),
    chatContainerRef,
    sentinelRef: autoScrollHelper.sentinelRef,
    sendMessage,
    clearHistory,
    scrollToBottom: autoScrollHelper.smoothScrollToBottom,
  }
}
