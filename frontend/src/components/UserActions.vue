<template>
  <v-btn>
    <v-menu activator="parent">
      <v-list>
        <v-list-item @click="logout"> Logout </v-list-item>
      </v-list>
    </v-menu>
    <v-avatar icon="mdi-account"> </v-avatar>
    <p>{{ user.first_name }}</p>
    <v-icon> mdi-menu-down </v-icon>
  </v-btn>
</template>
<script setup>
import { inject } from "@vue/runtime-core";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/user";

const axios = inject("axios");
const router = useRouter();
const user = useUserStore();

const logout = () => {
  axios
    .post("auth/logout")
    .catch((err) => {
      console.log(err);
    })
    .finally(() => {
      router.push("/login");
    });
};
</script>

