<template>
  <q-layout view="hhh lpR fFf">
    <q-header reveal bordered class="bg-primary text-white flex justify-center">
      <q-toolbar>
        <q-toolbar-title class="text-center">
          Find your partner
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <partner-card />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import PartnerCard from 'src/components/PartnerCard.vue';
</script>