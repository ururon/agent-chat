<script setup lang="ts">
import type { ChatMessage } from '~/types/chat'

interface Props {
  messages: readonly ChatMessage[]
  containerRef?: HTMLElement | null
}

defineProps<Props>()
</script>

<template>
  <div class="flex-1 overflow-y-auto p-4 bg-gray-50">
    <div v-if="messages.length === 0" class="flex items-center justify-center h-full text-gray-400">
      <div class="text-center">
        <div class="text-4xl mb-4">💬</div>
        <p>開始對話吧！</p>
      </div>
    </div>
    <div v-else class="max-w-4xl mx-auto">
      <ChatMessage
        v-for="(message, index) in messages"
        :key="index"
        :message="message"
      />
    </div>
  </div>
</template>
