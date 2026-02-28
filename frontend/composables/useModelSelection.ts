import { ref, computed, onMounted, readonly } from 'vue'
import type { Model } from '~/types/chat'

export const useModelSelection = () => {
  const API_BASE_URL = 'http://localhost:8000'

  // 狀態
  const models = ref<Model[]>([])
  const selectedModel = ref<string>('gemini-2-0-flash') // 預設值
  const isLoadingModels = ref(false)
  const modelsError = ref<string | null>(null)

  // 計算屬性
  const currentModel = computed(() => {
    return models.value.find((m) => m.id === selectedModel.value)
  })

  // 從 LocalStorage 恢復選擇
  const loadSavedModel = () => {
    if (process.client) {
      const saved = localStorage.getItem('selectedGeminiModel')
      if (saved) {
        selectedModel.value = saved
      }
    }
  }

  // 保存選擇到 LocalStorage
  const saveModelSelection = (modelId: string) => {
    selectedModel.value = modelId
    if (process.client) {
      localStorage.setItem('selectedGeminiModel', modelId)
    }
  }

  // 從後端取得模型列表
  const fetchModels = async () => {
    isLoadingModels.value = true
    modelsError.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/models`)

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: 無法取得模型列表`)
      }

      const data = await response.json()
      models.value = data.models

      // 驗證保存的選擇是否有效
      const validModelIds = models.value.map((m) => m.id)
      if (!validModelIds.includes(selectedModel.value)) {
        selectedModel.value = data.default_model
      }
    } catch (err) {
      console.error('取得模型列表失敗:', err)
      modelsError.value =
        err instanceof Error ? err.message : '無法載入模型列表'
      // 降級：使用預設值
      selectedModel.value = 'gemini-2-0-flash'
    } finally {
      isLoadingModels.value = false
    }
  }

  // 初始化
  onMounted(() => {
    loadSavedModel()
    fetchModels()
  })

  return {
    // 狀態
    models: readonly(models),
    selectedModel: readonly(selectedModel),
    currentModel,
    isLoadingModels: readonly(isLoadingModels),
    modelsError: readonly(modelsError),

    // 方法
    setSelectedModel: saveModelSelection,
    refreshModels: fetchModels,
  }
}
