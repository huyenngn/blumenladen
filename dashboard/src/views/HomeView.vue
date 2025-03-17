<script setup lang="ts">
import CardButton from '@/components/CardButton.vue';
import { RouterLink } from 'vue-router';

const links = [
    {
        to: '/inventory',
        icon: 'pi pi-box',
        text: 'Preisverzeichnis',
    },
    {
        to: '/reports',
        icon: 'pi pi-chart-bar',
        text: 'Berichte',
    },
];

</script>

<template>
    <nav class="grid grid-cols-2 gap-4 p-4 self-center">
        <RouterLink v-for="link in links" :key="link.to" :to="link.to">
            <CardButton :icon="link.icon" :text="link.text" />
        </RouterLink>
    </nav>
</template>
