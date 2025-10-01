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
} from '/wasm-client/pkg/aurora_wasm_client.js?v=2';

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
      this.updateDID(did);
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

  updateDID(did) {
    // Update short DID in info row (if element exists in future)
    const didEl = document.getElementById('did');
    if (didEl) {
      didEl.textContent = did.slice(0, 20) + '...';
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
      setupIdentityUI();
    }
  });/**
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
   * Setup identity UI and action buttons
   */
  function setupIdentityUI() {
    console.log('Setting up identity UI...');
    
    const identityPanel = document.getElementById('identity-panel');
    const didFullEl = document.getElementById('did-full');
    const identityTypeEl = document.getElementById('identity-type');
    
    console.log('Identity panel element:', identityPanel);
    console.log('Portal agent:', portal.agent);
    
    if (identityPanel && portal.agent) {
      // Show identity panel
      identityPanel.style.display = 'block';
      console.log('✅ Identity panel displayed');
      
      // Display full DID
      const did = portal.agent.get_did();
      if (didFullEl) didFullEl.textContent = did;
      if (identityTypeEl) identityTypeEl.textContent = 'Decentralized';
      
      // Test Signature button
      const btnSignTest = document.getElementById('btn-sign-test');
      if (btnSignTest) {
        btnSignTest.addEventListener('click', async () => {
          try {
            btnSignTest.disabled = true;
            btnSignTest.textContent = '🔐 Signing...';
            
            const message = `Test signature from ${did} at ${new Date().toISOString()}`;
            console.log('📝 Signing message:', message);
            
            const signature = await portal.agent.sign_message(message);
            console.log('✅ Signature:', signature.substring(0, 32) + '...');
            console.log('   Length:', signature.length / 2, 'bytes');
            
            // Verify
            const { verify_signature } = await import('/wasm-client/pkg/aurora_wasm_client.js?v=2');
            const publicKey = portal.agent.get_public_key();
            const isValid = await verify_signature(publicKey, message, signature);
            
            if (isValid) {
              alert(`✅ Signature Test Successful!\n\nMessage: ${message.substring(0, 60)}...\n\nSignature: ${signature.substring(0, 40)}...\n\nLength: ${signature.length / 2} bytes\n\nVerification: VALID ✓`);
            } else {
              alert('❌ Signature verification failed!');
            }
            
          } catch (error) {
            console.error('Signature test failed:', error);
            alert('❌ Signature test failed: ' + error.message);
          } finally {
            btnSignTest.disabled = false;
            btnSignTest.textContent = '🖊️ Test Signature';
          }
        });
      }
      
      // Export Identity button
      const btnExport = document.getElementById('btn-export-identity');
      if (btnExport) {
        btnExport.addEventListener('click', () => {
          try {
            const did = portal.agent.get_did();
            const publicKey = portal.agent.get_public_key();
            
            const identity = {
              version: '1.0',
              did: did,
              publicKey: JSON.parse(publicKey),
              algorithm: 'ECDSA-P256',
              created: new Date().toISOString(),
              note: 'Private key remains in browser localStorage. This export contains only public information.'
            };
            
            const blob = new Blob([JSON.stringify(identity, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `aurora-identity-${did.split(':').pop().substring(0, 8)}.json`;
            a.click();
            URL.revokeObjectURL(url);
            
            console.log('✅ Identity exported (public key only)');
          } catch (error) {
            console.error('Export failed:', error);
            alert('❌ Export failed: ' + error.message);
          }
        });
      }
      
      // Reset Identity button
      const btnReset = document.getElementById('btn-reset-identity');
      if (btnReset) {
        btnReset.addEventListener('click', async () => {
          const confirmed = confirm(
            '⚠️ WARNING: Reset Identity?\n\n' +
            'This will delete your current decentralized identity.\n' +
            'You will lose access to:\n' +
            '- Your DID\n' +
            '- Your signing keys\n' +
            '- Any reputation associated with this identity\n\n' +
            'A new identity will be generated on next reload.\n\n' +
            'Are you sure?'
          );
          
          if (confirmed) {
            try {
              // Clear localStorage
              localStorage.removeItem('aurora_identity');
              localStorage.removeItem('aurora_private_key_jwk');
              
              console.log('✅ Identity reset. Reloading...');
              alert('✅ Identity deleted. Page will reload to generate a new identity.');
              
              window.location.reload();
            } catch (error) {
              console.error('Reset failed:', error);
              alert('❌ Reset failed: ' + error.message);
            }
          }
        });
      }
    }
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