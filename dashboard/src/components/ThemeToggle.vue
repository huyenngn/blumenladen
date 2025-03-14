<script lang="ts" setup>
import { Button } from 'primevue';
import { ref } from 'vue';

const darkMode = ref(false);

const toggleDarkMode = () => {
    darkMode.value = !darkMode.value;
    document.body.classList.toggle('dark');
};
</script>

<template>
    <Button :icon="darkMode ? 'pi pi-moon' : 'pi pi-sun'" @click="toggleDarkMode" variant="text" />
</template>