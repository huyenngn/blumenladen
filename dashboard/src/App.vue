<script setup lang="ts">
import Button from 'primevue/button';
import ThemeToggle from './components/ThemeToggle.vue';

</script>

<template>
    <header class="flex items-stretch justify-stretch p-4">
        <div class="w-1/3 flex  items-center  justify-start">
            <Button severity="secondary" label="Back" icon="pi pi-angle-left" @click="$router.go(-1)"
                :class="{ 'hidden': $route.path === '/' }" />
        </div>
        <div class="flex items-center flex-1 justify-center">
            <h1 class="text-2xl font-bold">{{ $route.name }}</h1>
        </div>
        <div class="w-1/3 flex justify-end  items-center  ">
            <ThemeToggle />
        </div>
    </header>
    <main class="flex-1 flex justify-center items-center p-4">
        <RouterView />
    </main>
</template>
