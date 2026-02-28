import { ref, onUnmounted, readonly, nextTick, type Ref } from 'vue'
import { useDebounceFn } from '@vueuse/core'

/**
 * useAutoScroll - 自動滾動管理 Composable
 *
 * 負責管理聊天訊息容器的自動滾動邏輯
 *
 * @param containerRef - 滾動容器的 ref（必須有 overflow-y: auto）
 *
 * 使用要求：
 * 1. containerRef 必須指向有 overflow-y: auto/scroll 的 DOM 元素
 * 2. Sentinel 元素必須位於容器內部（用於 IntersectionObserver 偵測）
 * 3. 容器必須有固定或受限的高度
 *
 * 行為說明：
 * - IntersectionObserver 監聽容器底部，判斷用戶是否在底部
 * - 用戶主動滾動時暫停自動滾動（300ms 防抖）
 * - 新訊息到達時平滑滾動到底部
 * - 逐字渲染時防抖滾動（100ms）避免過度更新
 */
export const useAutoScroll = (containerRef: Ref<HTMLElement | null>) => {
  // 用戶是否在底部
  const isAtBottom = ref(true)

  // 用戶是否主動滾動中
  const isUserScrolling = ref(false)

  // Sentinel 元素 ref(用於 IntersectionObserver)
  const sentinelRef = ref<HTMLElement | null>(null)

  // IntersectionObserver 實例
  let observer: IntersectionObserver | null = null

  /**
   * 設置 IntersectionObserver 監聽底部
   * 當 Sentinel 進入視口時,表示用戶已滾到底部
   */
  const setupIntersectionObserver = () => {
    if (!sentinelRef.value || !containerRef.value) return

    observer = new IntersectionObserver(
      (entries) => {
        isAtBottom.value = entries[0].isIntersecting
      },
      {
        threshold: 0.1,
        root: containerRef.value, // 相對於滾動容器計算
      }
    )

    observer.observe(sentinelRef.value)
  }

  /**
   * 設置用戶滾動偵測
   * 用戶主動滾動時,停止自動滾動
   */
  const setupScrollListener = () => {
    if (!containerRef.value) return

    let scrollTimeout: ReturnType<typeof setTimeout> | null = null

    const handleScroll = () => {
      isUserScrolling.value = true

      // 300ms 未有滾動事件後,認為用戶停止滾動
      if (scrollTimeout) clearTimeout(scrollTimeout)
      scrollTimeout = setTimeout(() => {
        isUserScrolling.value = false
      }, 300)
    }

    containerRef.value.addEventListener('scroll', handleScroll, { passive: true })

    onUnmounted(() => {
      containerRef.value?.removeEventListener('scroll', handleScroll)
      if (scrollTimeout) clearTimeout(scrollTimeout)
    })
  }

  /**
   * 滾動到底部
   */
  const scrollToBottom = async (smooth = false) => {
    await nextTick()

    if (!containerRef.value) return

    containerRef.value.scrollTo({
      top: containerRef.value.scrollHeight,
      behavior: smooth ? 'smooth' : 'auto',
    })
  }

  /**
   * 平滑滾動到底部(平滑動畫)
   */
  const smoothScrollToBottom = () => {
    return scrollToBottom(true)
  }

  /**
   * 防抖的自動滾動(用於逐字時持續滾動)
   * 100ms 內只滾動一次
   */
  const debouncedAutoScroll = useDebounceFn(() => {
    // 如果用戶在滾動,不要強制滾動
    if (isUserScrolling.value) return

    // 使用平滑滾動
    scrollToBottom(true)
  }, 100)

  /**
   * 初始化滾動偵測
   */
  const init = () => {
    setupIntersectionObserver()
    setupScrollListener()
  }

  /**
   * 清理資源
   */
  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
    }
  })

  return {
    // 狀態
    isAtBottom: readonly(isAtBottom),
    isUserScrolling: readonly(isUserScrolling),
    sentinelRef,

    // 方法
    init,
    scrollToBottom,
    smoothScrollToBottom,
    debouncedAutoScroll,
  }
}
