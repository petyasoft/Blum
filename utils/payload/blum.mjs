import { Blum } from './blum_worker.mjs';

const gameId = process.argv[2];
const points = parseInt(process.argv[3]);
const trump = parseInt(process.argv[4]);
const harris = parseInt(process.argv[5]);
const freeze = parseInt(process.argv[6]);
const total = points + ((trump + harris) * 5);
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
            amount: total,
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
        },
        TRUMP: {
            clicks: trump
        },
        HARRIS: {
            clicks: harris
        }
    }
);
console.log(payload);
