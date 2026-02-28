/**
 * 訊息角色類型
 */
export type MessageRole = 'user' | 'assistant'

/**
 * 聊天訊息介面
 */
export interface ChatMessage {
  role: MessageRole
  content: string
  timestamp: Date
}

/**
 * API 請求：發送訊息
 */
export interface SendMessageRequest {
  message: string
}

/**
 * SSE 事件類型
 */
export type SSEEventType = 'chunk' | 'done' | 'error'

/**
 * SSE 事件資料
 */
export interface SSEEvent {
  event: SSEEventType
  data: string
}

/**
 * 錯誤回應
 */
export interface ErrorResponse {
  detail: string
}
