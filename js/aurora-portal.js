/**
 * Aurora WASM Client Integration
 * 
 * This file demonstrates how to integrate the Aurora WASM client
 * with the existing Aurora Portal web interface.
 */

import init, { 
  create_agent, 
  get_version, 
  health_check,
  AuroraAgent 
} from './wasm-client/pkg/aurora_wasm_client.js';

class AuroraPortal {
  constructor() {
    this.agent = null;
    this.config = {
      relay_nodes: [
        '/dns4/relay1.aurora.network/tcp/443/wss/p2p/12D3KooWABC',
        '/dns4/relay2.aurora.network/tcp/443/wss/p2p/12D3KooWDEF'
      ],
      blockchain_rpc: 'https://rpc.aurora.network',
      bootstrap_models: [
        '0x1234abcd...', // Discovery model
        '0x5678ef01...', // Negotiation model
        '0x9012cdef...'  // Security model
      ],
      user_did: null
    };
  }

  /**
   * Initialize the Aurora Portal
   */
  async initialize() {
    try {
      console.log('Initializing Aurora Portal...');
      
      // Show loading state
      this.showStatus('Initializing...', 'info');

      // Initialize WASM module
      await init();
      console.log('WASM module loaded successfully');
      console.log('Aurora Client Version:', get_version());
      console.log('Health check:', health_check());

      // Create Aurora agent
      this.agent = await create_agent(JSON.stringify(this.config));
      console.log('Aurora Agent created');

      // Start the agent (connect to P2P + blockchain)
      await this.agent.start();
      console.log('Aurora Agent started');

      // Get agent info
      const did = this.agent.get_did();
      const peerCount = this.agent.get_peer_count();
      const state = this.agent.get_state();

      console.log('Agent DID:', did);
      console.log('Connected peers:', peerCount);
      console.log('Agent state:', state);

      // Update UI
      this.showStatus(`Connected as ${did.slice(0, 20)}...`, 'success');
      this.updatePeerCount(peerCount);
      this.enableChat();

      return true;
    } catch (error) {
      console.error('Failed to initialize Aurora Portal:', error);
      this.showStatus('Failed to initialize: ' + error.message, 'error');
      return false;
    }
  }

  /**
   * Process user prompt
   */
  async processPrompt(prompt) {
    if (!this.agent) {
      throw new Error('Agent not initialized');
    }

    try {
      this.showStatus('Processing...', 'info');
      
      const result = await this.agent.process_prompt(prompt);
      
      this.showStatus('Ready', 'success');
      return result;
    } catch (error) {
      console.error('Failed to process prompt:', error);
      this.showStatus('Error: ' + error.message, 'error');
      throw error;
    }
  }

  /**
   * Get current agent state
   */
  getState() {
    if (!this.agent) return null;
    return this.agent.get_state();
  }

  /**
   * Shutdown the portal
   */
  async shutdown() {
    if (this.agent) {
      try {
        await this.agent.shutdown();
        console.log('Aurora Agent shut down');
      } catch (error) {
        console.error('Error shutting down agent:', error);
      }
    }
  }

  // UI Helper methods
  showStatus(message, type) {
    const statusEl = document.getElementById('status');
    if (statusEl) {
      statusEl.textContent = message;
      statusEl.className = `status ${type}`;
    }
    console.log(`[${type.toUpperCase()}] ${message}`);
  }

  updatePeerCount(count) {
    const peerCountEl = document.getElementById('peer-count');
    if (peerCountEl) {
      peerCountEl.textContent = count;
    }
  }

  enableChat() {
    const chatInput = document.getElementById('chat-input');
    const chatButton = document.getElementById('chat-button');
    
    if (chatInput) chatInput.disabled = false;
    if (chatButton) chatButton.disabled = false;
  }
}

// Global portal instance
let portal = null;

/**
 * Initialize Aurora Portal when page loads
 */
window.addEventListener('DOMContentLoaded', async () => {
  console.log('Aurora Portal loading...');
  
  portal = new AuroraPortal();
  
  // Initialize portal
  const success = await portal.initialize();
  
  if (success) {
    console.log('Aurora Portal ready!');
    setupEventListeners();
  }
});

/**
 * Setup UI event listeners
 */
function setupEventListeners() {
  const chatButton = document.getElementById('chat-button');
  const chatInput = document.getElementById('chat-input');

  if (chatButton && chatInput) {
    chatButton.addEventListener('click', async () => {
      const prompt = chatInput.value.trim();
      if (!prompt) return;

      try {
        const result = await portal.processPrompt(prompt);
        displayMessage('user', prompt);
        displayMessage('agent', result);
        chatInput.value = '';
      } catch (error) {
        displayMessage('system', 'Error: ' + error.message);
      }
    });

    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatButton.click();
      }
    });
  }
}

/**
 * Display a chat message
 */
function displayMessage(role, content) {
  const chatHistory = document.getElementById('chat-history');
  if (!chatHistory) return;

  const messageEl = document.createElement('div');
  messageEl.className = `message ${role}`;
  messageEl.textContent = content;
  
  chatHistory.appendChild(messageEl);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

/**
 * Cleanup on page unload
 */
window.addEventListener('beforeunload', () => {
  if (portal) {
    portal.shutdown();
  }
});

// Export for external use
export { AuroraPortal, portal };
