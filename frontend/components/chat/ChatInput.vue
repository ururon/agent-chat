<script setup lang="ts">
import { ref } from 'vue'

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

const isFocused = ref(false)
</script>

<template>
  <div class="relative z-10 px-4 py-4 pb-6">
    <!-- Floating Input Container -->
    <div
      :class="[
        'glass-effect p-4 transition-all duration-300',
        isFocused && 'border-white/40 bg-white/15'
      ]"
    >
      <div class="flex gap-3 items-end">
        <!-- Textarea -->
        <div class="flex-1 relative">
          <textarea
            v-model="inputMessage"
            :disabled="disabled"
            placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
            rows="3"
            class="w-full glass-input px-4 py-3 text-sm rounded-xl resize-none transition-all duration-300"
            @keydown="handleKeydown"
            @compositionstart="handleCompositionStart"
            @compositionend="handleCompositionEnd"
            @focus="isFocused = true"
            @blur="isFocused = false"
          />
        </div>

        <!-- Send Button -->
        <button
          :disabled="disabled || !inputMessage.trim()"
          @click="handleSend"
          :class="[
            'group relative flex-shrink-0 w-12 h-12 rounded-full',
            'transition-all duration-300 font-medium text-sm',
            'disabled:opacity-50 disabled:cursor-not-allowed',
            'overflow-hidden'
          ]"
        >
          <!-- Button Background Gradient -->
          <div
            :class="[
              'absolute inset-0 bg-gradient-to-r from-cyan-400 to-indigo-600',
              'transition-all duration-300',
              disabled || !inputMessage.trim() ? 'opacity-50' : 'opacity-100 group-hover:opacity-110 group-active:scale-95'
            ]"
          ></div>

          <!-- Button Icon -->
          <div class="relative flex items-center justify-center h-full text-white text-lg">
            <transition
              name="rotate"
              mode="out-in"
            >
              <span v-if="disabled" key="loading" class="animate-typing">⚙️</span>
              <span v-else key="send">➤</span>
            </transition>
          </div>
        </button>
      </div>

      <!-- Help Text -->
      <p class="text-xs text-white/40 mt-2 ml-4">
        {{ disabled ? '⏳ Processing your message...' : '💡 Tip: Shift+Enter for new line' }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.glass-input {
  @apply bg-white/5 backdrop-blur-md border border-white/20 text-white placeholder-white/40;

  &:focus {
    @apply border-cyan-400/50 bg-white/10 outline-none ring-0;
  }

  &:disabled {
    @apply opacity-60 cursor-not-allowed;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
