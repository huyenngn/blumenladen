<script lang="ts" setup>
import { list_flowers } from '@/lib/data';
import { onMounted, ref } from 'vue';

const inventory = ref([]);




onMounted(() => {
    inventory.value = list_flowers().then((data) => {
        return data;
    });
});


</script>

<template>
    <div>
        <h1>Inventory</h1>
    </div>
</template>