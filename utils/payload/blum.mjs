import { Blum } from './blum_worker.mjs';

const gameId = process.argv[2];
const points = parseInt(process.argv[3]);
const freeze = parseInt(process.argv[4]);
const challenge = Blum.getChallenge(gameId);
const uuidChallenge = Blum.getUUID();

const payload = Blum.getPayload(
    gameId,
    {
        id: uuidChallenge,
        nonce: challenge.nonce,
        hash: challenge.hash,
    },
    {
        BP: {
            amount: points,
        }
    },
    {
        CLOVER: {
            clicks: points
        },
        FREEZE: {
            clicks: freeze
        },
        BOMB: {
            clicks: 0
        }
    }
);
console.log(payload);
