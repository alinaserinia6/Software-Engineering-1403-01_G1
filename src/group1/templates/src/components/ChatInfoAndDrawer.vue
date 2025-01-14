<template>
  <q-layout view="hHh lpr lFf">
  
    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
  
        <q-toolbar-title class="text-center">
          user name
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
  
      <q-drawer v-model="leftDrawerOpen" side="left"  elevated>
        <q-list>
        <q-item v-for="chat in chats"
          :key="chat.id"
          clickable
          @click="selectChat(chat.id)"
        >
          <q-item-section>{{ chat.title }}</q-item-section>
        </q-item>
        <q-item>
          <h1>salam</h1>
        </q-item>
      </q-list>
      </q-drawer>
  
      <q-page-container>
        <router-view />
      </q-page-container>
  
    </q-layout>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  // import { useChatStore } from '../stores/chatStore';
  
  const leftDrawerOpen = ref(false)
  function toggleLeftDrawer() {
    leftDrawerOpen.value = !leftDrawerOpen.value
  }
  
  // const chatStore = useChatStore();
  // const chats = chatStore.chats;
  // const selectChat = chatStore.selectChat;
  </script>