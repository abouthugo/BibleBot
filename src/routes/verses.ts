import Context from '../models/context';
import Version from '../models/version';

import * as utils from '../helpers/verse_utils';

export class VersesRouter {
    private static instance: VersesRouter;

    private constructor() {
        // nothing to see here, move along
    }

    static getInstance(): VersesRouter {
        if (!VersesRouter.instance) {
            VersesRouter.instance = new VersesRouter();
        }

        return VersesRouter.instance;
    }

    processMessage(ctx: Context, inputType: string): void {
        // get rid of newlines and instead put a space between lines
        const msg = ctx.msg.split(/\r?\n/).join(' ');
        
        if (!msg.includes(' ')) { return; }

        const results = utils.findBooksInMessage(msg);

        if (results.length > 10) {
            ctx.channel.send(ctx.language.getString('donutspam'));
            ctx.logInteraction('err', ctx.shard, ctx.id, ctx.channel, 'spam attempt');
            return;
        }

        results.forEach((result) => {
            if (utils.isSurroundedByBrackets(ctx.guildPreferences.ignoringBrackets, result, msg)) {
                return;
            }

            if (inputType == 'erasmus' && !utils.isSurroundedByBrackets('[]', result, msg)) {
                return;
            }

            let queryVersion = 'RSV';
            if (ctx.preferences.version) {
                queryVersion = ctx.preferences.version;
            }

            Version.findOne({ abbv: queryVersion }, async (err, version) => {
                const reference = await utils.generateReference(result, ctx.msg.split(/\r?\n/).join(' '), version);

                if (reference === null) {
                    return;
                }

                utils.processVerse(ctx, reference.version, reference);
            });
        }); 
    }
}