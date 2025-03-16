<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import type { TotalCosts } from '@/lib/types'
import { get_costs } from '@/lib/api'

const costs = ref<TotalCosts[]>([])

onMounted(async () => {
    costs.value = await get_costs("month", "2021-01-01", "2024-12-31")
})
</script>

<template>
    <div>
        {{ costs }}
    </div>
</template>