<script lang="ts" setup>
import { list_flowers } from '@/lib/data';
import type { Flower } from '@/lib/types';
import { onMounted, ref } from 'vue';

const inventory = ref<Flower[]>([]);

onMounted(async () => {
    inventory.value = await list_flowers();
});
</script>

<template>
    <div>
        <h1>Inventory</h1>
    </div>
</template>