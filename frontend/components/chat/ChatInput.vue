<script setup lang="ts">
interface Props {
  disabled?: boolean
}

interface Emits {
  (e: 'send', message: string): void
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false
})

const emit = defineEmits<Emits>()

const inputMessage = ref('')
const isComposing = ref(false)

const handleSend = () => {
  const message = inputMessage.value.trim()
  if (message && !props.disabled) {
    emit('send', message)
    inputMessage.value = ''
  }
}

const handleKeydown = (event: KeyboardEvent) => {
  // 在 IME 合成過程中，不觸發 Enter 事件
  if (event.isComposing || isComposing.value) return

  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSend()
  }
}

const handleCompositionStart = () => {
  isComposing.value = true
}

const handleCompositionEnd = () => {
  isComposing.value = false
}
</script>

<template>
  <div class="border-t bg-white p-4">
    <div class="flex gap-2">
      <textarea
        v-model="inputMessage"
        :disabled="disabled"
        placeholder="輸入訊息... (Enter 發送, Shift+Enter 換行)"
        rows="3"
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
        @keydown="handleKeydown"
        @compositionstart="handleCompositionStart"
        @compositionend="handleCompositionEnd"
      />
      <button
        :disabled="disabled || !inputMessage.trim()"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors h-fit self-end"
        @click="handleSend"
      >
        {{ disabled ? '發送中...' : '發送' }}
      </button>
    </div>
  </div>
</template>
