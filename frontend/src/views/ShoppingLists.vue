<template>
  <v-card>
    <v-card-title> Minhas listas </v-card-title>
    <v-card-text>
      <v-data-table :headers="headers" :items="lists" @click:row.prevent="openDetails">
        <template v-slot:item.created_at="{ item }">
          {{ dayjs(item.raw.created_at).format("YYYY-MM-DD") }}
        </template>
        <template v-slot:item.updated_at="{ item }">
          {{ dayjs(item.raw.updated_at).format("YYYY-MM-DD") }}
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
<script setup>
import { inject, onMounted, ref } from "@vue/runtime-core";
import dayjs from "dayjs";
import { useRouter } from "vue-router";

const router = useRouter();
const axios = inject("axios");

const lists = ref([]);
const headers = [
  { key: "name", title: "Name" },
  { key: "created_at", title: "Created at" },
  { key: "updated_at", title: "Updated at" }]

function formatDate(date) {
  return dayjs(date).format("YYYY/MM/DD");
}

function openDetails(item, data) {
  return router.push(`/shopping-list/${data.item.raw.id}`);
}

onMounted(() => {
  axios.get("shopping-lists").then((resp) => {
    lists.value = resp.data
  });
});
</script>