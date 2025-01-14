<template>
  <div class="chat-input-container" :class="{ 'drawer-open': isDrawerOpen }">
    <q-btn icon="mic" class="icon-button" @click="startRecording" />
    <q-btn icon="attach_file" class="icon-button" @click="attachFile" />
    <input class="chat-input" type="text" placeholder="Type a message..." />
    <q-btn icon="send" class="send-button" @click="send" />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

// Accept drawer state as a prop
defineProps({
  isDrawerOpen: {
    type: Boolean,
    required: true
  }
});

// const startRecording = () => {
//   console.log('Voice recording started');
//   // Add your recording logic here
// };

// const attachFile = () => {
//   console.log('Attach file dialog opened');
//   // Add your file attachment logic here
// };
</script>

<style scoped>
.chat-input-container {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: margin-left 0.3s ease, width 0.3s ease;
  background: #f9f9f9;
  padding: 15px;
  border-radius: 25px;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.chat-input-container.drawer-open {
  margin-left: 250px; /* Adjust based on drawer's width */
  width: calc(80% - 250px);
}

.chat-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 20px;
  font-size: 16px;
  outline: none;
}

.chat-input:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.icon-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 18px;
  cursor: pointer;
  padding: 10px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.icon-button:hover {
  background-color: #0056b3;
  color: white;
}

.send-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-button:hover {
  background-color: #0056b3;
}
</style>
