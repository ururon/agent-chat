<script setup lang="ts">
const {
  messages,
  isLoading,
  error,
  chatContainerRef,
  sendMessage,
  clearHistory
} = useChat()

const handleSend = (message: string) => {
  sendMessage(message)
}

const handleClear = async () => {
  if (confirm('確定要清除所有對話記錄嗎？')) {
    await clearHistory()
  }
}

// 設定頁面 meta
useHead({
  title: 'AI Chat - 智能對話助手'
})
</script>

<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-800">
          🤖 AI Chat 助手
        </h1>
        <button
          v-if="messages.length > 0"
          @click="handleClear"
          class="px-4 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
        >
          清除對話
        </button>
      </div>
    </header>

    <!-- Error Alert -->
    <div
      v-if="error"
      class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mx-4 mt-4 rounded"
      role="alert"
    >
      <p class="font-bold">錯誤</p>
      <p>{{ error }}</p>
    </div>

    <!-- Chat Container -->
    <div class="flex-1 overflow-hidden">
      <div
        ref="chatContainerRef"
        class="h-full overflow-y-auto"
      >
        <ChatContainer :messages="messages" />
      </div>
    </div>

    <!-- Input Area -->
    <ChatInput
      :disabled="isLoading"
      @send="handleSend"
    />
  </div>
</template>
