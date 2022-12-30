<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="mx-auto" max-width="600">
          <v-card-title> Login </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col>
                  <v-snackbar v-model="diag">
                    <v-alert :text="text" type="error" />
                  </v-snackbar>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-text-field v-model="username" label="Username" />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-text-field
                    v-model="password"
                    label="Password"
                    type="password"
                    persistent-clear
                  />
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click.prevent="submit">Login</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import router from "@/router";
import { inject, ref } from "vue";
import { useUserStore } from "@/store/user";
import qs from "qs";

const axios = inject("axios");
const user = useUserStore();
const username = ref("");
const password = ref("");
const diag = ref(false);
const text = ref("");

const submit = () => {
  axios
    .post(
      "auth/login",
      qs.stringify({
        username: username.value,
        password: password.value,
      })
    )
    .then((resp) => {
      localStorage.setItem("access_token", resp.data.access_token);
      localStorage.setItem("refresh_token", resp.data.refresh_token);
      router.push("/");
    })
    .then(() => {
      axios.get("auth/me").then((resp) => {
        user.first_name = resp.data.first_name;
        router.push("");
      });
    })
    .catch((err) => {
      diag.value = true;
      text.value = err.response.data.detail;
    });
};
</script>