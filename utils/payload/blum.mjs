import { Blum } from './blum_worker.mjs';

const gameId = process.argv[2];
const points = parseInt(process.argv[3]);
const freeze = parseInt(process.argv[4]);
const challenge = Blum.getChallenge(gameId);
const uuidChallenge = Blum.getUUID();

const payload = Blum.getPayload(
    gameId,
    {
        hash: challenge.hash,
        id: uuidChallenge,
        nonce: challenge.nonce,
    },
    {
        BP: {
            amount: points,
        }
    },
    {
        BOMB: {
            clicks: 0
        },
        CLOVER: {
            clicks: points
        },
        FREEZE: {
            clicks: freeze
        }
    }
);
console.log(payload);
