import type { ChatMessage, SendMessageRequest } from '~/types/chat'

export const useChat = () => {
  // 狀態管理
  const messages = ref<ChatMessage[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const chatContainerRef = ref<HTMLElement | null>(null)

  // API 基礎 URL
  const API_BASE_URL = 'http://localhost:8000'

  /**
   * 自動滾動到最新訊息
   */
  const autoScroll = () => {
    nextTick(() => {
      if (chatContainerRef.value) {
        chatContainerRef.value.scrollTop = chatContainerRef.value.scrollHeight
      }
    })
  }

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
    autoScroll()

    // 準備 AI 訊息佔位
    const aiMessage: ChatMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date()
    }
    messages.value.push(aiMessage)
    const aiMessageIndex = messages.value.length - 1

    try {
      // 發送 POST 請求
      const response = await fetch(`${API_BASE_URL}/api/chat/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message.trim() } as SendMessageRequest),
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

      while (true) {
        const { done, value } = await reader.read()

        if (done) break

        // 解碼 chunk
        buffer += decoder.decode(value, { stream: true })
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
          if (eventType === 'chunk' && eventData) {
            try {
              const parsed = JSON.parse(eventData)
              if (parsed.content) {
                // 使用陣列索引更新，確保 Vue 能偵測到變化
                const currentMessage = messages.value[aiMessageIndex]
                messages.value[aiMessageIndex] = {
                  ...currentMessage,
                  content: currentMessage.content + parsed.content
                }
                autoScroll()
              }
            } catch (e) {
              console.error('解析 chunk 失敗:', e)
            }
          } else if (eventType === 'done') {
            isLoading.value = false
            break
          } else if (eventType === 'error' && eventData) {
            try {
              const errorObj = JSON.parse(eventData)
              throw new Error(errorObj.error || '未知錯誤')
            } catch (e) {
              throw new Error(eventData)
            }
          }
        }
      }

    } catch (err) {
      console.error('發送訊息錯誤:', err)
      error.value = err instanceof Error ? err.message : '發送訊息失敗'

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
    } catch (err) {
      console.error('清除歷史錯誤:', err)
      error.value = err instanceof Error ? err.message : '清除歷史失敗'
    }
  }

  return {
    messages: readonly(messages),
    isLoading: readonly(isLoading),
    error: readonly(error),
    chatContainerRef,
    sendMessage,
    clearHistory,
  }
}
