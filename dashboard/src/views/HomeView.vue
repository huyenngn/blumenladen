<script setup lang="ts">
import CardButton from '@/components/CardButton.vue';
import { RouterLink } from 'vue-router';

</script>

<template>
    <nav class="grid grid-cols-2 gap-4 p-4">
        <RouterLink to="/inventory">
            <CardButton>
                <i class="pi pi-box"></i>
                <span>Preisverzeichnis</span>
            </CardButton>
        </RouterLink>
        <RouterLink to="/reports">
            <CardButton>
                <i class="pi pi-chart-bar"></i>
                <span>Berichte</span>
            </CardButton>
        </RouterLink>
    </nav>
</template>
