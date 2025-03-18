<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps({
    icon: {
        type: String,
    },
    text: {
        type: String,
    },
});

</script>

<template>
    <div
        class="aspect-3/2 rounded-lg bg-secondary text-2xl font-medium text-secondary-foreground flex justify-center items-center gap-2 p-8">
        <i :class="props.icon"></i>
        <span>{{ props.text }}</span>
    </div>
</template>