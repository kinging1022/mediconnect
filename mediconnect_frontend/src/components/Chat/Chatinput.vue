<template>
    <form @submit.prevent="handleSubmit" class="fixed bottom-0 left-0 right-0 flex gap-2 p-4 border-t bg-white z-10">
      <!-- File input -->
      <input
        type="file"
        ref="fileInput"
        @change="handleFileSelect"
        accept="image/*,video/*"
        class="hidden"
        multiple
      />
  
      <div class="flex-1 flex flex-col">
        <!-- Preview area -->
        <div v-if="selectedFiles.length" class="mb-2 flex gap-2">
          <div v-for="(file, index) in selectedFiles" :key="index" class="relative">
            <img
              v-if="file.type.startsWith('image')"
              :src="file.preview"
              class="h-20 w-20 object-cover rounded"
            />
            <video
              v-else-if="file.type.startsWith('video')"
              :src="file.preview"
              class="h-20 w-20 object-cover rounded"
            />
            <button
              @click="removeFile(index)"
              class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
            >
              <x-icon size="12" />
            </button>
          </div>
        </div>
  
        <!-- Text input -->
        <div class="flex gap-2">
          <button
            type="button"
            @click="$refs.fileInput.click()"
            class="p-2 text-gray-500 hover:text-gray-700"
          >
            <paperclip-icon size="20" />
          </button>
  
          <textarea
            :value="modelValue"
            @input="handleInput"
            @keypress="handleKeyPress"
            @blur="handleBlur"
            :placeholder="sessionEnded ? 'This session has ended' : 'Type your message...'"
            :disabled="sessionEnded"
            class="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
  
          <button
            type="submit"
            :disabled="sessionEnded || (!modelValue.trim() && !selectedFiles.length)"
            :class="[
              'p-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors',
              sessionEnded && 'cursor-not-allowed opacity-50'
            ]"
          >
            <send-icon size="20" />
          </button>
        </div>
      </div>
    </form>
  </template>
  
  <script>
  import { SendIcon, PaperclipIcon, XIcon } from 'lucide-vue-next';
  
  export default {
    name: 'ChatInput',
    components: {
      SendIcon,
      PaperclipIcon,
      XIcon,
    },
    props: {
      modelValue: {
        type: String,
        required: true,
      },
      sessionEnded: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        typingTimeout: null,
        isTyping: false,
        selectedFiles: [],
      };
    },
    methods: {
      // File handling
      async handleFileSelect(event) {
        const files = Array.from(event.target.files);
  
        for (const file of files) {
          if (file.size > 10 * 1024 * 1024) { // 10MB limit
            this.$emit('error', 'File size should not exceed 10MB');
            continue;
          }
  
          const preview = URL.createObjectURL(file);
          this.selectedFiles.push({
            file,
            preview,
            type: file.type,
          });
        }
  
        event.target.value = ''; // Reset input
      },
      removeFile(index) {
        URL.revokeObjectURL(this.selectedFiles[index].preview);
        this.selectedFiles.splice(index, 1);
      },
  
      // Form submission
      async handleSubmit() {
        if (this.sessionEnded) return;
  
        if (this.selectedFiles.length) {
          // If we have files, create FormData
          const formData = new FormData();
  
          // Add text message if present
          if (this.modelValue.trim()) {
            formData.append('message', this.modelValue.trim());
          }
  
          // Add files with correct keys
          this.selectedFiles.forEach((file, index) => {
            formData.append(`file_${index}`, file.file);
          });
  
          // Emit the send event with the formData
          this.$emit('send', formData);
        } else if (this.modelValue.trim()) {
          // If we only have text, emit as plain text (not FormData)
          this.$emit('send', this.modelValue.trim());
        }
  
        // Clear the input text (emit event to update the v-model)
        this.$emit('update:modelValue', '');
  
        // Clean up selected files
        this.selectedFiles.forEach(file => {
          URL.revokeObjectURL(file.preview);
        });
        this.selectedFiles = [];
        this.stopTyping();
      },
  
      // Input handling
      handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey && !this.sessionEnded) {
          e.preventDefault();
          this.handleSubmit(); // Call handleSubmit directly instead of emitting 'send'
        }
      },
      handleInput(e) {
        this.$emit('update:modelValue', e.target.value);
        this.startTyping();
      },
      handleBlur() {
        this.stopTyping();
      },
  
      // Typing indicator
      startTyping() {
        if (!this.isTyping) {
          console.log('Emitting typing start'); // Debug log
          this.isTyping = true;
          this.$emit('typing', true);
        }
        if (this.typingTimeout) {
          clearTimeout(this.typingTimeout);
        }
        this.typingTimeout = setTimeout(() => {
          this.stopTyping();
        }, 1500);
      },
      stopTyping() {
        if (this.isTyping) {
          console.log('Emitting typing stop'); // Debug log
          this.isTyping = false;
          this.$emit('typing', false);
          if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
            this.typingTimeout = null;
          }
        }
      },
    },
    beforeUnmount() {
      this.stopTyping();
    },
  };
  </script>