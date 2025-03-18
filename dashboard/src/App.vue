<script setup lang="ts">
import ThemeToggle from '@/components/ThemeToggle.vue';
import Button from 'primevue/button';
import { RouterView } from 'vue-router';

</script>

<template>
    <header class="fixed top-0 inset-x-0 flex items-stretch justify-stretch p-4 z-10 bg-background">
        <div class="w-1/3 flex items-center justify-start">
            <Button severity="secondary" label="Zurück" icon="pi pi-angle-left" @click="$router.go(-1)"
                :class="{ 'hidden': $route.path === '/' }" />
        </div>
        <div class="flex items-center flex-1 justify-center">
            <h1 class="text-2xl font-bold">{{ $route.name }}</h1>
        </div>
        <div class="w-1/3 flex justify-end items-center  ">
            <ThemeToggle />
        </div>
    </header>
    <main class="flex-1 flex justify-center items-start px-4 pb-4 pt-19 min-h-dvh">
        <RouterView />
    </main>
</template>
