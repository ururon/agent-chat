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
  <div class="relative flex flex-col h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900">
    <!-- Decorative Blur Orbs -->
    <div class="absolute -top-40 -left-40 w-80 h-80 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
    <div class="absolute -bottom-40 right-20 w-80 h-80 bg-gradient-to-br from-cyan-400 to-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-float" style="animation-delay: 2s;"></div>
    <div class="absolute top-1/2 left-1/2 w-96 h-96 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style="animation-delay: 4s;"></div>

    <!-- Header -->
    <header class="relative z-10 glass-effect mx-4 mt-4 mb-4 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-cyan-300 via-indigo-300 to-purple-300 bg-clip-text text-transparent">
            ✨ AI Nexus
          </h1>
          <p class="text-xs text-white/60 mt-1">Powered by Gemini Intelligence</p>
        </div>
        <button
          v-if="messages.length > 0"
          @click="handleClear"
          class="group relative px-6 py-2 text-sm font-medium text-white transition-all duration-300 overflow-hidden rounded-full"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-red-500 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <span class="relative flex items-center gap-2">
            🗑️ Clear
          </span>
        </button>
      </div>
    </header>

    <!-- Error Alert -->
    <transition name="slide-down" mode="out-in">
      <div
        v-if="error"
        class="relative z-10 mx-4 mb-4 glass-effect px-6 py-4 border-l-4 border-red-500/50"
        role="alert"
      >
        <p class="text-sm font-semibold text-red-300">⚠️ Error</p>
        <p class="text-sm text-red-200/80 mt-1">{{ error }}</p>
      </div>
    </transition>

    <!-- Chat Container -->
    <div class="relative z-10 flex-1 overflow-hidden rounded-t-3xl bg-white/5 backdrop-blur-md border-t border-white/10">
      <div
        ref="chatContainerRef"
        class="h-full overflow-y-auto scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent"
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

<style scoped>
/* Custom scrollbar styling */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
