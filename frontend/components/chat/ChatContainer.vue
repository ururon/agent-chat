<script setup lang="ts">
import type { ChatMessage } from '~/types/chat'

interface Props {
  messages: readonly ChatMessage[]
  containerRef?: HTMLElement | null
}

defineProps<Props>()
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Empty State -->
    <div v-if="messages.length === 0" class="flex-1 flex items-center justify-center">
      <div class="text-center animate-slide-up">
        <div class="text-6xl mb-6">🚀</div>
        <h2 class="text-2xl font-bold bg-gradient-to-r from-cyan-300 to-purple-300 bg-clip-text text-transparent mb-3">
          Welcome to AI Nexus
        </h2>
        <p class="text-white/60 mb-8 text-sm max-w-xs">
          Start a conversation with our intelligent AI assistant powered by Google Gemini
        </p>

        <!-- Feature Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-8 px-4">
          <div class="glass-effect p-4 rounded-xl transition-all duration-300 hover:border-white/40">
            <div class="text-2xl mb-2">💡</div>
            <p class="text-xs text-white/80">Smart Insights</p>
          </div>
          <div class="glass-effect p-4 rounded-xl transition-all duration-300 hover:border-white/40">
            <div class="text-2xl mb-2">⚡</div>
            <p class="text-xs text-white/80">Fast & Reliable</p>
          </div>
          <div class="glass-effect p-4 rounded-xl transition-all duration-300 hover:border-white/40">
            <div class="text-2xl mb-2">🎯</div>
            <p class="text-xs text-white/80">Precise Answers</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div v-else class="flex-1 overflow-y-auto p-4 sm:p-6">
      <div class="max-w-3xl mx-auto space-y-4">
        <ChatMessage
          v-for="(message, index) in messages"
          :key="index"
          :message="message"
        />
      </div>
    </div>
  </div>
</template>
