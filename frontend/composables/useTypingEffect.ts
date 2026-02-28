/**
 * useTypingEffect - 打字機效果 Composable
 *
 * 實現字符隊列機制，將收到的文字逐字渲染，產生平滑的打字機效果。
 * 用於 AI 回覆的 Streaming 顯示。
 */

export const useTypingEffect = (typingSpeed: number = 40) => {
  // 已渲染的文字
  const typedText = ref('')

  // 字符隊列
  const queue = ref<string[]>([])

  // 定時器 ID
  const typingInterval = ref<ReturnType<typeof setInterval> | null>(null)

  // 是否正在打字中
  const isTyping = ref(false)

  /**
   * 將文字拆分為字符並加入隊列
   */
  const enqueueCharacters = (text: string) => {
    if (!text) return
    queue.value.push(...text.split(''))
  }

  /**
   * 開始逐字渲染
   */
  const startTyping = () => {
    if (typingInterval.value) return // 避免重複啟動

    isTyping.value = true

    typingInterval.value = setInterval(() => {
      if (queue.value.length > 0) {
        const char = queue.value.shift()
        if (char !== undefined) {
          typedText.value += char
        }
      } else {
        // 隊列空了但仍在等待更多字符，不停止
        // 只有 stopTyping() 被呼叫時才真正停止
      }
    }, typingSpeed)
  }

  /**
   * 停止打字效果，並立即渲染隊列中剩餘的所有字符
   */
  const stopTyping = () => {
    if (typingInterval.value) {
      clearInterval(typingInterval.value)
      typingInterval.value = null
    }

    // 立即渲染剩餘字符
    if (queue.value.length > 0) {
      typedText.value += queue.value.join('')
      queue.value = []
    }

    isTyping.value = false
  }

  /**
   * 重置所有狀態
   */
  const reset = () => {
    stopTyping()
    typedText.value = ''
    queue.value = []
  }

  /**
   * 取得當前隊列長度（用於 debug）
   */
  const queueLength = computed(() => queue.value.length)

  // 組件卸載時清理定時器
  onUnmounted(() => {
    if (typingInterval.value) {
      clearInterval(typingInterval.value)
    }
  })

  return {
    // 狀態
    typedText: readonly(typedText),
    isTyping: readonly(isTyping),
    queueLength,

    // 方法
    enqueueCharacters,
    startTyping,
    stopTyping,
    reset
  }
}
