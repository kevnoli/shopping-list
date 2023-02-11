<template>
  <div>
    <v-app-bar color="primary">
      <v-app-bar-nav-icon @click="navbar = !navbar"></v-app-bar-nav-icon>
      <v-app-bar-title> Shopping Lists </v-app-bar-title>
      <v-spacer />
      <user-actions />
    </v-app-bar>
    <v-navigation-drawer v-model="navbar" temporary>
      <v-list nav>
        <v-list-item prepend-icon="mdi-format-list-checks" title="Shopping lists" value="shopping-lists"
          @click="pushRoute('/shopping-lists')" />
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script setup>
import { ref } from "@vue/reactivity";
import UserActions from "@/components/UserActions.vue";
import { useRouter } from "vue-router";

const router = useRouter()

const navbar = ref(false);

function pushRoute(route_name) {
  router.push(route_name)
  navbar.value = false
}
</script>
