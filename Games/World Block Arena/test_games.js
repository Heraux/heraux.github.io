// Automated game tester — runs inside the browser via preview_eval
// Returns a results object with bugs found

(async function runTests(){
  const GAMES = 20;
  const MATCHUPS = [
    ['medieval','jurassic'], ['jurassic','medieval'],
    ['city','space'], ['space','city'],
    ['medieval','city'], ['city','medieval'],
    ['jurassic','space'], ['space','jurassic'],
    ['medieval','space'], ['space','medieval'],
    ['city','jurassic'], ['jurassic','city'],
    ['medieval','medieval'], ['city','city'],
    ['jurassic','jurassic'], ['space','space'],
    ['medieval','jurassic'], ['city','space'],
    ['jurassic','city'], ['space','medieval'],
  ];

  const results = [];
  const bugs = [];

  for(let g = 0; g < GAMES; g++){
    const [pDeck, aDeck] = MATCHUPS[g % MATCHUPS.length];
    const gameResult = { game: g+1, pDeck, aDeck, rounds: 0, winner: null, errors: [], warnings: [] };

    try {
      // Reset game state
      document.getElementById('gameScreen').classList.add('active');
      initGame(pDeck, aDeck);

      // Remove any overlays
      const ov = document.getElementById('activePickOverlay');
      if(ov) ov.remove();

      // Auto-pick active for player (first bench card)
      if(G.player.bench.length > 0){
        const pick = G.player.bench[0];
        G.player.bench = G.player.bench.filter(c => c.uid !== pick.uid);
        G.player.active = pick;
      }

      // Simulate up to 30 rounds
      let safetyCounter = 0;
      while(!G.over && safetyCounter < 300){
        safetyCounter++;
        G.phase = 'play';
        G.currentTurn = 'player';
        G.player.passed = false;
        G.ai.passed = false;

        // Clear any leftover flags
        [G.player, G.ai].forEach(p => {
          p.noMove = false;
          p.holdTheLine = false;
          p._stampede = false;
          p._blockOppMove = false;
          p._loseBlockMove = false;
          p._noActions = false;
          p._sieged = false;
          p._ironWill = false;
          p._blitz = false;
          p._quantumEntangle = false;
          p._embedded = false;
        });

        // === PLAYER TURN: simple AI-like logic ===
        // Try upgrade
        const pUpgrades = G.player.hand.filter(c => canUpgrade(c, G.player.active, G.playerDeck)).sort((a,b) => b.power - a.power);
        if(pUpgrades.length > 0){
          try { applyUpgrade(G.player, pUpgrades[0], 'player'); }
          catch(e){ gameResult.errors.push(`P upgrade error: ${e.message}`); }
        }

        // Try an action
        const pActions = G.player.hand.filter(c => c.type === 'action');
        if(pActions.length > 0 && !G.player._noActions){
          // Just play first valid action (simple)
          for(const act of pActions){
            try {
              // Basic legality checks
              if(act.effect === 'kings_declaration' && G.player.active?.id !== 'king') continue;
              if(act.effect === 'coronation' && !G.player.hand.some(h => h.id === 'king')) continue;
              if(act.effect === 'wormhole' && G.player.active?.id !== 'phenomenon') continue;
              if(act.effect === 'rip_in_spacetime' && (G.player.active?.id !== 'phenomenon' || G.player.bench.length > 0)) continue;
              if(act.effect === 'dispatch' && G.player.active?.id !== 'officer' && G.player.active?.id !== 'police_chief') continue;
              if(act.effect === 'backdraft' && G.player.active?.id !== 'firefighter') continue;
              if(act.effect === 'block_transport' && G.player.active?.id !== 'captain') continue;
              if(act.effect === 'block_tractor' && G.player.active?.id !== 'farmer') continue;
              if(act.effect === 'block_mayor' && (G.player.active?.level !== 1 || G.player.active?.deck !== 'city')) continue;
              if(act.effect === 'search_action' && G.player.active?.level !== 1) continue;
              if(act.effect === 'dino_roar' && (G.player.active?.level !== 1 || !G.player.hand.some(h => h.type === 'chain' && h.level === 3))) continue;
              if(act.effect === 'to_the_beginning' && !G.player.hand.some(h => h.type === 'chain' && h.level === 3)) continue;
              if(act.effect === 'last_stand' && G.player.bench.length > 0) continue;
              if(act.effect === 'scholarly' && G.player.bench.length === 0) continue;
              if(act.effect === 'event_horizon' && G.player.pos < 15) continue;
              if(act.effect === 'embedded' && (G.player.active?.id !== 'spore' || G.player.active?.level !== 2)) continue;
              if(act.effect === 'quantum_tunneling' && G.player.active?.id !== 'ai_overlord' && G.player.active?.id !== 'phenomenon') continue;
              playActionCard(G.player, act, 'player');
              break;
            } catch(e){
              gameResult.errors.push(`P action ${act.effect} error: ${e.message}`);
            }
          }
        }

        G.player.passed = true;

        // === AI TURN ===
        G.currentTurn = 'ai';
        try {
          // Run AI logic directly (not async)
          if(!G.ai.cannotPlayNext){
            const assess = aiAssess();
            const plan = aiPlan(assess);

            // Upgrades
            const aiUp = G.ai.hand.filter(c => canUpgrade(c, G.ai.active, G.aiDeck) && !G.ai._sieged).sort((a,b) => b.power - a.power);
            if(aiUp.length > 0){
              applyUpgrade(G.ai, aiUp[0], 'ai');
            }

            // Actions
            const aiActions = G.ai.hand.filter(c => c.type === 'action' && !G.ai._noActions);
            if(aiActions.length > 0){
              const pick = pickAIAction(aiActions, G.ai, plan, assess);
              if(pick){
                try { playActionCard(G.ai, pick, 'ai'); }
                catch(e){ gameResult.errors.push(`AI action ${pick.effect} error: ${e.message}`); }
              }
            }

            // Post-action upgrades
            const aiUp2 = G.ai.hand.filter(c => canUpgrade(c, G.ai.active, G.aiDeck) && !G.ai._sieged).sort((a,b) => b.power - a.power);
            if(aiUp2.length > 0){
              applyUpgrade(G.ai, aiUp2[0], 'ai');
            }
          }
          G.ai.passed = true;
        } catch(e){
          gameResult.errors.push(`AI turn error: ${e.message}`);
          G.ai.passed = true;
        }

        // === RESOLVE ===
        try {
          aiDecidePowerPool();
          // Simple resolve (skip cinematic)
          const pPow = (G.player.active?.power || 0) + (G.player._powerBoost || 0);
          const aPow = (G.ai.active?.power || 0) + (G.ai._powerBoost || 0);

          if(G.meteorPlayed){
            G.meteorPlayed = false;
          } else if(pPow > aPow){
            const moveAmt = pPow;
            G.player.pos = Math.min(30, G.player.pos + moveAmt);
            // On-win effects
            try { applyOnWin(G.player, G.player.active, 'player'); } catch(e){ gameResult.errors.push(`P onWin error: ${e.message}`); }
          } else if(aPow > pPow){
            const moveAmt = aPow;
            G.ai.pos = Math.min(30, G.ai.pos + moveAmt);
            try { applyOnWin(G.ai, G.ai.active, 'ai'); } catch(e){ gameResult.errors.push(`AI onWin error: ${e.message}`); }
          }
          // Tie: no movement

          // Check win by position
          if(G.player.pos >= 30){ G.over = true; G.winner = 'player'; break; }
          if(G.ai.pos >= 30){ G.over = true; G.winner = 'ai'; break; }
        } catch(e){
          gameResult.errors.push(`Resolve error: ${e.message}`);
        }

        // === CLEANUP ===
        try {
          // Discard actives
          const pKeep = G.player._keepActive;
          const aKeep = G.ai._keepActive;
          if(!pKeep){
            if(G.player.active) G.player.discard.push(G.player.active);
            G.player.active = null;
          }
          if(!aKeep){
            if(G.ai.active) G.ai.discard.push(G.ai.active);
            G.ai.active = null;
          }

          // Clear round flags
          [G.player, G.ai].forEach(p => {
            p.stack.forEach(c => p.discard.push(c)); p.stack = [];
            p.passed = false;
            p._powerBoost = 0;
            p._keepActive = false;
            p._explorerKeep = false;
            p._kingsBanner = false;
            p._kingCouncilBonusApplied = false;
          });

          // Bench-out check
          const pOut = !pKeep && G.player.bench.length === 0;
          const aOut = !aKeep && G.ai.bench.length === 0;
          if(pOut || aOut){
            G.over = true;
            G.winner = G.player.pos >= G.ai.pos ? 'player' : 'ai';
            gameResult.warnings.push(`Bench-out: pOut=${pOut} aOut=${aOut}`);
            break;
          }

          // Pick new actives
          if(!aKeep || !G.ai.active){
            try { aiPickActive(); }
            catch(e){ gameResult.errors.push(`aiPickActive error: ${e.message}`); }
          }
          if(!pKeep || !G.player.active){
            if(G.player.bench.length > 0){
              const pick = G.player.bench[0];
              G.player.bench = G.player.bench.filter(c => c.uid !== pick.uid);
              G.player.active = pick;
            }
          }

          // Validate state
          if(!G.player.active && G.player.bench.length === 0){
            G.over = true; G.winner = 'ai';
            gameResult.warnings.push('Player has no active and no bench');
            break;
          }
          if(!G.ai.active && G.ai.bench.length === 0){
            G.over = true; G.winner = 'player';
            gameResult.warnings.push('AI has no active and no bench');
            break;
          }

          // Resupply
          G.round++;
          gameResult.rounds = G.round;

          // Discard personal cards
          [G.player, G.ai].forEach(p => {
            p.hand = p.hand.filter(c => c.deck !== 'personal');
          });

          // Draw up to 5
          [G.player, G.ai].forEach(p => {
            const need = Math.max(0, 5 - p.hand.length);
            if(need > 0) drawCards(p, need);
          });

        } catch(e){
          gameResult.errors.push(`Cleanup error: ${e.message}`);
          break;
        }
      }

      if(safetyCounter >= 300 && !G.over){
        gameResult.errors.push('INFINITE LOOP — game never ended after 300 iterations');
        G.over = true;
      }

      gameResult.winner = G.winner;
      gameResult.pPos = G.player.pos;
      gameResult.aPos = G.ai.pos;
      gameResult.rounds = G.round;

    } catch(e){
      gameResult.errors.push(`GAME CRASH: ${e.message}\n${e.stack}`);
    }

    results.push(gameResult);
    if(gameResult.errors.length > 0){
      bugs.push(...gameResult.errors.map(e => `Game ${g+1} (${pDeck} vs ${aDeck}): ${e}`));
    }
  }

  // Summary
  const wins = results.filter(r => r.winner === 'player').length;
  const losses = results.filter(r => r.winner === 'ai').length;
  const avgRounds = Math.round(results.reduce((s,r) => s + r.rounds, 0) / GAMES);
  const errorGames = results.filter(r => r.errors.length > 0).length;

  return {
    summary: `${GAMES} games: Player ${wins} wins, AI ${losses} wins. Avg ${avgRounds} rounds. ${errorGames} games with errors.`,
    bugs: bugs,
    gameDetails: results.map(r => `G${r.game} ${r.pDeck}v${r.aDeck}: ${r.winner} wins R${r.rounds} (${r.pPos}-${r.aPos}) ${r.errors.length>0?'⚠️'+r.errors.length+'err':'✅'} ${r.warnings.join(', ')}`),
    errorDetails: bugs
  };
})();
