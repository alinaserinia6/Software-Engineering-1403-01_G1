<template>
    <div class="chat-room-container">
      <div class="drawer-container" :class="{ 'drawer-open': isDrawerOpen }">
        <chat-info-and-drawer :is-drawer-open="isDrawerOpen"
          @toggle-drawer="toggleDrawer" />
      </div>
  
      <div class="chat-content-container">
        <chat-window />
        <message-input :is-drawer-open="isDrawerOpen" @sendMessage="handleSendMessage" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import ChatInfoAndDrawer from '../components/ChatInfoAndDrawer.vue';
  import ChatWindow from '../components/ChatWindow.vue';
  import MessageInput from '../components/MessageInput.vue';
  
  const isDrawerOpen = ref(false);
  
  function toggleDrawer() {
    isDrawerOpen.value = !isDrawerOpen.value;
  }
  </script>
  
  <style scoped>
  .chat-room-container {
    display: flex;
    height: 100vh;
    overflow: hidden;
  }
  
  .drawer-container {
    width: 0;
    transition: width 0.3s ease;
    overflow: hidden;
  }
  
  .drawer-container.drawer-open {
    width: 250px; /* Adjust based on the drawer's width */
  }
  
  .chat-content-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-left: 0;
    transition: margin-left 0.3s ease;
  }
  </style>
  