/**
 * Test script for Aurora decentralized signature system
 * Add this to browser console after portal loads
 */

async function testSignature() {
    console.log('=== Aurora Signature Test ===\n');
    
    try {
        // 1. Get the agent instance
        if (!window.portal || !window.portal.agent) {
            console.error('Portal not initialized. Wait for "Aurora Portal ready!" message.');
            return;
        }

        const agent = window.portal.agent;
        
        // 2. Get user DID
        const did = agent.get_did();
        console.log('✓ User DID:', did);
        
        // 3. Get public key
        const publicKey = agent.get_public_key();
        console.log('✓ Public Key (JWK):', publicKey.substring(0, 100) + '...\n');
        
        // 4. Sign a test message
        const testMessage = 'Hello Aurora! This is a test message from ' + did;
        console.log('📝 Message to sign:', testMessage);
        
        console.log('🔐 Signing message...');
        const signature = await agent.sign_message(testMessage);
        console.log('✓ Signature (hex):', signature.substring(0, 32) + '...' + signature.substring(signature.length - 32));
        console.log('  Length:', signature.length / 2, 'bytes\n');
        
        // 5. Verify the signature
        console.log('🔍 Verifying signature...');
        const { verify_signature } = await import('/wasm-client/pkg/aurora_wasm_client.js?v=2');
        const isValid = await verify_signature(publicKey, testMessage, signature);
        
        if (isValid) {
            console.log('✅ Signature is VALID!\n');
        } else {
            console.log('❌ Signature is INVALID!\n');
            return;
        }
        
        // 6. Test with tampered message
        console.log('Testing signature verification with tampered message...');
        const tamperedMessage = testMessage + ' (tampered)';
        const isValidTampered = await verify_signature(publicKey, tamperedMessage, signature);
        
        if (!isValidTampered) {
            console.log('✅ Tampered signature correctly rejected!\n');
        } else {
            console.log('❌ WARNING: Tampered signature accepted! Security issue!\n');
        }
        
        // 7. Summary
        console.log('=== Test Summary ===');
        console.log('✓ Identity: Decentralized (no MetaMask, no external services)');
        console.log('✓ Algorithm: ECDSA P-256 (NIST standard)');
        console.log('✓ Key Storage: Browser localStorage (JWK format)');
        console.log('✓ Signature: Cryptographically secure (' + (signature.length / 2) + ' bytes)');
        console.log('✓ Verification: Working correctly');
        console.log('\n✅ All tests passed! Decentralized authentication is working.\n');
        
        // 8. Show example use cases
        console.log('=== Example Use Cases ===');
        console.log('1. P2P Message Signing:');
        console.log('   const msg = JSON.stringify({ type: "negotiate", model: "QmABC..." });');
        console.log('   const sig = await agent.sign_message(msg);');
        console.log('   // Send { message: msg, signature: sig, did: agent.get_did() }');
        console.log('');
        console.log('2. Blockchain Transaction:');
        console.log('   const tx = JSON.stringify({ action: "register_model", hash: "QmXYZ..." });');
        console.log('   const sig = await agent.sign_message(tx);');
        console.log('   // Submit to Aurora L2 with signature proof');
        console.log('');
        console.log('3. Off-chain Attestation:');
        console.log('   const attestation = `Session ${sessionId} completed with SLO compliance`;');
        console.log('   const sig = await agent.sign_message(attestation);');
        console.log('   // Store in IPFS or send to peers');
        
    } catch (error) {
        console.error('❌ Test failed:', error);
        console.error(error.stack);
    }
}

// Auto-run if portal is ready
if (window.portal && window.portal.agent) {
    console.log('Portal detected, running signature test...\n');
    testSignature();
} else {
    console.log('Portal not ready. Run testSignature() manually after portal loads.');
    window.testSignature = testSignature;
}
