<template>
  <v-card>
    <v-card-title> Minhas listas </v-card-title>
    <v-card-text>
      <v-list lines="two">
        <v-list-item
          v-for="item in lists"
          :key="item.id"
          :title="item.name"
          :subtitle="formatDate(item.created_at)"
          @click="shoppingListDetails(item.id)"
        />
      </v-list>
    </v-card-text>
  </v-card>
</template>
<script setup>
import { inject, onMounted, reactive } from "@vue/runtime-core";
import dayjs from "dayjs";
import { useRouter } from "vue-router";

const router = useRouter();

const axios = inject("axios");
const lists = reactive([]);

function formatDate(date) {
  return dayjs(date).format("YYYY/MM/DD");
}

function shoppingListDetails(id) {
  return router.push(`/shopping-lists/${id}`);
}

onMounted(() => {
  axios.get("shopping-lists").then((resp) => {
    Object.assign(lists, resp.data);
  });
});
</script>