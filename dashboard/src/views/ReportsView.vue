<script lang="ts" setup>
import { get_costs } from '@/lib/api'
import type { TotalCost } from '@/lib/types'
import { formatCurrency, formatMonth } from '@/lib/utils'
import { onMounted, ref } from 'vue'

const costs = ref<TotalCost[]>([])

onMounted(async () => {
    costs.value = await get_costs("month", "2021-01-01", "2025-03-17")
})
</script>

<template>
    <div>
        <div v-for="cost in costs" :key="cost.group_by">
            {{ formatMonth(cost.group_by) }}: {{ formatCurrency(cost.cost) }}
        </div>
    </div>
</template>