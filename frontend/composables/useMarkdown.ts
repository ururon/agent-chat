import { marked } from 'marked'
import DOMPurify from 'dompurify'

/**
 * Markdown 渲染 Composable
 * 提供安全的 Markdown 轉 HTML 功能
 */
export const useMarkdown = () => {
  // 配置 marked 選項
  marked.setOptions({
    gfm: true, // 啟用 GitHub Flavored Markdown
    breaks: true, // 將換行符轉換為 <br>
    headerIds: false, // 禁用標題 ID 以提高安全性
    mangle: false // 禁用 email 地址混淆
  })

  /**
   * 將 Markdown 內容轉換為安全的 HTML
   * @param content Markdown 格式的內容
   * @returns 經過清理的 HTML 字串
   */
  const renderMarkdown = (content: string): string => {
    if (!content) return ''

    try {
      // 使用 marked 解析 Markdown
      const rawHtml = marked.parse(content) as string

      // 使用 DOMPurify 清理 HTML，防止 XSS 攻擊
      const cleanHtml = DOMPurify.sanitize(rawHtml, {
        // 允許的標籤
        ALLOWED_TAGS: [
          'p', 'br', 'strong', 'em', 'u', 's', 'code', 'pre',
          'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
          'ul', 'ol', 'li',
          'blockquote',
          'table', 'thead', 'tbody', 'tr', 'th', 'td',
          'a', 'img'
        ],
        // 允許的屬性
        ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class'],
        // 允許的 URI schemes
        ALLOWED_URI_REGEXP: /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
      })

      return cleanHtml
    } catch (error) {
      console.error('Markdown 渲染錯誤:', error)
      // 如果渲染失敗，返回純文本
      return content
    }
  }

  return {
    renderMarkdown
  }
}
