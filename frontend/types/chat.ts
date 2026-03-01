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
  model?: string
}

/**
 * Gemini 模型介面
 */
export interface Model {
  id: string
  name: string
  category: 'advanced' | 'recommended' | 'stable'
  description: string
}

/**
 * AI 模型詳細資訊（對應後端 ModelInfo）
 */
export interface ModelInfo {
  id: string
  name: string
  category: string
  description: string
  context_window: number
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
