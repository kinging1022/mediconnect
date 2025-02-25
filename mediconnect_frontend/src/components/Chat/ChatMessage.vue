<template>
    <div 
      class="flex-1 overflow-y-auto p-4 mt-16 mb-20" 
      ref="messagesContainer"
    >
      <div v-for="message in messages" :key="message.id">
        <MessageItem :message="message" />
      </div>
  
      <Typingindicator v-if="isTyping" />
      
      <div ref="messagesEnd"></div>
    </div>
  </template>
  
  <script>
  import MessageItem from './MessageItem.vue'
  import Typingindicator from './Typingindicator.vue'
  
  export default {
    name: 'ChatMessages',
    components: {
        MessageItem,
      Typingindicator
    },
    props: {
      messages: {
        type: Array,
        required: true
      },
      isTyping: {
        type: Boolean,
        default: false
      }
    },
    watch: {
      messages: {
        handler() {
          this.scrollToBottom()
        },
        deep: true
      },
      isTyping() {
        this.scrollToBottom()
      }
    },
    methods: {
      scrollToBottom() {
        this.$nextTick(() => {
          this.$refs.messagesEnd.scrollIntoView({ behavior: 'smooth' })
        })
      }
    }
  }
  </script>
  
  