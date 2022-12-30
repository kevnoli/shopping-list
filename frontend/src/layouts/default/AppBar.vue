<template>
  <div>
    <v-app-bar color="primary">
      <v-app-bar-nav-icon @click="navbar = !navbar"></v-app-bar-nav-icon>
      <v-app-bar-title> Shopping Lists </v-app-bar-title>
      <v-spacer />
      <user-actions />
    </v-app-bar>
    <v-navigation-drawer v-model="navbar"></v-navigation-drawer>
  </div>
</template>

<script setup>
import { ref } from "@vue/reactivity";
import UserActions from "@/components/UserActions.vue";

const navbar = ref(false);
</script>
