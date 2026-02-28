<script setup lang="ts">
import type { ChatMessage } from '~/types/chat'

interface Props {
  message: ChatMessage
}

const props = defineProps<Props>()

// 引入 Markdown 渲染功能
const { renderMarkdown } = useMarkdown()

// 格式化時間
const formattedTime = computed(() => {
  return props.message.timestamp.toLocaleTimeString('zh-TW', {
    hour: '2-digit',
    minute: '2-digit'
  })
})

// 根據角色決定樣式
const messageClass = computed(() => {
  return props.message.role === 'user'
    ? 'bg-blue-500 text-white ml-auto'
    : 'bg-gray-200 text-gray-800 mr-auto'
})

const containerClass = computed(() => {
  return props.message.role === 'user'
    ? 'justify-end'
    : 'justify-start'
})

// 為 AI 訊息渲染 Markdown
const renderedContent = computed(() => {
  if (props.message.role === 'assistant') {
    return renderMarkdown(props.message.content)
  }
  return props.message.content
})
</script>

<template>
  <div class="flex mb-4" :class="containerClass">
    <div class="max-w-[70%] rounded-lg px-4 py-2 shadow-md" :class="messageClass">
      <div class="text-sm opacity-75 mb-1">
        {{ message.role === 'user' ? '你' : 'AI 助理' }}
      </div>
      <!-- AI 訊息使用 Markdown 渲染 -->
      <div
        v-if="message.role === 'assistant'"
        class="prose prose-sm max-w-none prose-pre:bg-gray-800 prose-pre:text-gray-100 prose-code:text-pink-600 prose-a:text-blue-600 prose-strong:text-gray-900 prose-headings:text-gray-800"
        v-html="renderedContent"
      />
      <!-- 使用者訊息保持純文本 -->
      <div v-else class="whitespace-pre-wrap break-words">
        {{ message.content }}
      </div>
      <div class="text-xs opacity-60 mt-1 text-right">
        {{ formattedTime }}
      </div>
    </div>
  </div>
</template>
