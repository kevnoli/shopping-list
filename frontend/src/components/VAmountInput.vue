<template>
  <v-text-field v-model.lazy="formattedValue" ref="inputRef"></v-text-field>
</template>
<script>
import { watch } from "vue";
import { useCurrencyInput } from "vue-currency-input";

export default {
  name: "VAmountInput",
  props: {
    modelValue: Number,
    options: Object,
  },
  setup(props) {
    const options = {
      "currency": "USD",
      "currencyDisplay": "hidden",
      "valueRange": {
        "min": 0
      },
      "precision": 0,
      "autoDecimalDigits": true,
      ...props.options
    }
    const {
      inputRef,
      formattedValue,
      setValue,
    } = useCurrencyInput(options);

    watch(
      () => props.modelValue,
      (value) => {
        setValue(value);
      }
    );

    return { inputRef, formattedValue };
  },
};
</script>