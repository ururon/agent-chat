<template>
  <div class="relative">
    <!-- 選擇按鈕 - Header 版本 (緊湊) -->
    <button
      @click="toggleDropdown"
      class="px-4 py-2 text-sm font-medium bg-white/10 hover:bg-white/15 border border-white/20 rounded-lg text-white transition-all flex items-center gap-2 focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-transparent"
    >
      <span class="text-white/70">Model:</span>
      <span>{{ selectedModelName }}</span>
      <svg
        class="w-4 h-4 transition-transform flex-shrink-0"
        :class="{ 'rotate-180': isOpen }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
      </svg>
    </button>

    <!-- 下拉選單 -->
    <div
      v-if="isOpen"
      class="absolute top-full right-0 mt-2 min-w-[240px] rounded-lg shadow-xl z-50 bg-slate-900/95 backdrop-blur-md border border-white/15"
    >
      <!-- 滾軸限制容器：最多 5 筆，超過則顯示滾軸 -->
      <div class="max-h-[240px] overflow-y-auto">
        <button
          v-for="model in models"
          :key="model.id"
          @click="selectModel(model)"
          class="w-full px-4 py-3 text-left hover:bg-white/10 focus:outline-none focus:bg-white/10 transition-colors border-b border-white/5 last:border-b-0"
          :class="{ 'bg-white/15 font-semibold': isSelected(model.id) }"
        >
          <div class="flex justify-between items-center gap-3">
            <div class="flex-1">
              <div class="text-white font-medium">{{ model.name }}</div>
              <div class="text-xs text-white/60 mt-1">{{ model.category }}</div>
            </div>
            <svg
              v-if="isSelected(model.id)"
              class="w-5 h-5 text-cyan-400 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </button>
      </div>
    </div>
  </div>

  <!-- 點擊外部關閉下拉選單 -->
  <div
    v-if="isOpen"
    class="fixed inset-0 z-40"
    @click="isOpen = false"
  />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Model } from '~/types/chat'

interface Props {
  models: readonly Model[]
  modelValue: string
}

// 正確：只在 <script setup> 頂層呼叫一次
const props = defineProps<Props>()
defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const isOpen = ref(false)

// 使用 defineModel 進行雙向綁定
const selectedModelId = defineModel<string>('modelValue')

// 計算當前選擇的模型名稱
const selectedModelName = computed(() => {
  const selected = props.models.find(m => m.id === selectedModelId.value)
  return selected?.name || '選擇模型'
})

// 檢查是否為選中的模型
const isSelected = (modelId: string) => {
  return selectedModelId.value === modelId
}

// 選擇模型
const selectModel = (model: Model) => {
  selectedModelId.value = model.id
  isOpen.value = false
}

// 切換下拉選單
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}
</script>

<style scoped>
/* 自訂滾軸樣式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
