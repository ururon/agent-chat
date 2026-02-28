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

// 為 AI 訊息渲染 Markdown
const renderedContent = computed(() => {
  if (props.message.role === 'assistant') {
    return renderMarkdown(props.message.content)
  }
  return props.message.content
})

const isUser = computed(() => props.message.role === 'user')
</script>

<template>
  <div class="flex mb-4 animate-slide-up" :class="isUser ? 'justify-end' : 'justify-start'">
    <!-- AI Avatar -->
    <div v-if="!isUser" class="flex-shrink-0 mr-3">
      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-indigo-600 flex items-center justify-center text-sm font-bold">
        🤖
      </div>
    </div>

    <!-- Message Bubble -->
    <div
      :class="[
        'group max-w-xl px-4 py-3 rounded-2xl transition-all duration-300',
        isUser
          ? 'bg-gradient-to-br from-indigo-500 to-purple-600 text-white shadow-lg shadow-purple-500/20 hover:shadow-purple-500/40'
          : 'glass-effect hover:bg-white/15 hover:border-white/30'
      ]"
    >
      <!-- Role Label (AI only) -->
      <div v-if="!isUser" class="text-xs font-semibold text-white/70 mb-1">
        AI Nexus
      </div>

      <!-- Content -->
      <div
        v-if="isUser"
        class="text-sm whitespace-pre-wrap break-words"
      >
        {{ message.content }}
      </div>

      <!-- AI Markdown Content -->
      <div
        v-else
        class="prose prose-sm max-w-none dark:prose-invert
          prose-p:text-white/90 prose-p:text-sm prose-p:my-2
          prose-headings:text-white prose-headings:font-bold
          prose-strong:text-cyan-300 prose-em:text-purple-200
          prose-code:text-cyan-300 prose-code:bg-white/10 prose-code:px-2 prose-code:py-1 prose-code:rounded
          prose-pre:bg-slate-900/50 prose-pre:border prose-pre:border-white/20 prose-pre:rounded-lg prose-pre:p-4
          prose-a:text-cyan-300 prose-a:hover:text-cyan-200
          prose-ul:text-white/80 prose-li:text-white/80
          prose-blockquote:border-l-cyan-400 prose-blockquote:text-white/70"
        v-html="renderedContent"
      />

      <!-- Timestamp -->
      <div class="text-xs mt-2" :class="isUser ? 'text-white/60' : 'text-white/50'">
        {{ formattedTime }}
      </div>
    </div>

    <!-- User Avatar -->
    <div v-if="isUser" class="flex-shrink-0 ml-3">
      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 to-purple-600 flex items-center justify-center text-sm font-bold">
        👤
      </div>
    </div>
  </div>
</template>
