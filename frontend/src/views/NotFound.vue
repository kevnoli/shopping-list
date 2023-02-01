<template>

</template>
<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

onMounted(() => {
    // TODO: add alert
    router.push({ name: "home" })
})
</script>