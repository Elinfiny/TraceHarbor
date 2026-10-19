export function correctedNativeCaller125(preloaded, tools, save) {
  const bundle=preloaded.bundle;
  if (!['ADMIN125','SYNTHETIC_SOURCE_ONLY'].includes(bundle.mode)) throw Error('Administrative125 or explicit inert qualification only');
  const counts={launches:0,guardStarts:0,polls:0,writeCalls:0,libraryCalls:0,failed:false,first_unknown:null};
  let publication=null,holder=null;
  const fail=reason=>{counts.failed=true;counts.first_unknown??=reason;throw Error(counts.first_unknown);};
  const live=()=>{if(counts.failed||Date.now()>=bundle.deadline_utc_ms)fail('FirstUNKNOWN/original parent expired; no reset/retry');};
  // Closed recursive JSON grammar. JSON.parse alone silently accepts duplicate
  // keys and nonfinite exponent results, so it cannot authenticate guard output.
  const parseStrict=text=>{
    if(typeof text!=='string'||text.length>524288)throw Error('Bounded complete JSON');
    let i=0;const ws=()=>{while(/[\x20\t\r\n]/.test(text[i]||'!'))i++;};
    const string=()=>{const start=i;if(text[i++]!=='"')throw Error('String');while(i<text.length){const c=text[i++];if(c==='"')return JSON.parse(text.slice(start,i));if(c==='\\'){if(i>=text.length)throw Error('Truncated escape');i++;}else if(c.charCodeAt(0)<32)throw Error('Control character');}throw Error('Truncated string');};
    const value=()=>{ws();const c=text[i];if(c==='"')return string();if(c==='{'){i++;ws();const out=Object.create(null),keys=new Set();if(text[i]==='}'){i++;return out;}while(true){ws();const k=string();if(keys.has(k))throw Error('Duplicate key');keys.add(k);ws();if(text[i++]!==':')throw Error('Colon');out[k]=value();ws();const end=text[i++];if(end==='}')return out;if(end!==',')throw Error('Object delimiter');}}
      if(c==='['){i++;ws();const out=[];if(text[i]===']'){i++;return out;}while(true){out.push(value());ws();const end=text[i++];if(end===']')return out;if(end!==',')throw Error('Array delimiter');}}
      for(const [literal,result] of [['true',true],['false',false],['null',null]])if(text.startsWith(literal,i)){i+=literal.length;return result;}
      const m=text.slice(i).match(/^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/);if(!m)throw Error('JSON token');i+=m[0].length;const n=Number(m[0]);if(!Number.isFinite(n))throw Error('Nonfinite number');return n;};
    const result=value();ws();if(i!==text.length)throw Error('Extra/mixed output');return result;
  };
  const call=async(name,invoke)=>{
    let original;
    try{original=await invoke();}
    catch(error){await save(name,{tool_throw:{name:String(error?.name||'Error'),message:String(error?.message||error),stack:String(error?.stack||'').slice(0,16384)},status:'UNKNOWN_NO_RETRY'});fail('Native tool throw retained: '+name);}
    await save(name,original); // Always before a clock/parse/exit postguard.
    live();if(!original||original.isError===true)fail('Native original error retained: '+name);
    return original;
  };
  const pollOriginal=async(session,name)=>{
    live();if(!Number.isInteger(session)||counts.polls>=6||counts.writeCalls>=8)fail('Shared poll/write cap or session');
    counts.polls++;counts.writeCalls++;
    const original=await call(name,()=>tools.write_stdin({session_id:session,chars:'',yield_time_ms:1000,max_output_tokens:2500}));
    if(original.session_id!=null&&original.session_id!==session)fail('Foreign process session retained; no dependent effect');
    return original;
  };
  const awaitGuard=async seq=>{
    live();if(![1,2].includes(seq)||counts.guardStarts!==seq-1)fail('One guard launch per fixed step');
    counts.guardStarts++;
    let original=await call('guard'+seq+'-first.original.json',()=>tools.exec_command({...preloaded.guardDriver,cmd:preloaded.guardCommand+' '+seq}));
    const session=original.session_id;let complete=original.output||'';
    while(original.exit_code==null){
      if(!Number.isInteger(session)||original.session_id!==session)fail('No exact live original guard session');
      original=await pollOriginal(session,'guard'+seq+'-poll'+(counts.polls+1)+'.original.json');
      complete+=original.output||'';if(complete.length>524288)fail('Guard wholeoutput cap');
    }
    if(original.exit_code!==0)fail('Same guard nonzero terminal retained');
    try{parseStrict(complete);}catch(error){fail('Strict guard JSON: '+error.message);}
    return {...original,output:complete};
  };
  return {mode:bundle.mode,now:()=>Date.now(),save,parseStrict,counts,
    launch:async()=>{live();if(counts.launches++)fail('ONE actual holder only');const r=await call('caller-holder-start.original.json',()=>tools.exec_command(preloaded.driver));holder=r.session_id;if(!Number.isInteger(holder)||r.exit_code!=null)fail('Actual live holder required');return r;},
    verify:awaitGuard,
    poll:async session=>{if(session!==holder)fail('Foreign holder poll');return await pollOriginal(session,'caller-holder-poll'+(counts.polls+1)+'.original.json');},
    publicationOriginal:async()=>publication,
    tools:{apply_patch:tools.apply_patch,
      write_stdin:async args=>{live();if(args.session_id!==holder||typeof args.chars!=='string'||!args.chars||counts.writeCalls>=8)fail('Same holder one callback/cap');counts.writeCalls++;const r=await call('caller-callback'+counts.writeCalls+'.original.json',()=>tools.write_stdin(args));if(r.session_id!=null&&r.session_id!==holder)fail('Foreign holder callback return retained');return r;},
      mcp__codex_apps__library_replace_library_file:async args=>{live();counts.libraryCalls++;const r=await call('caller-library-replace.original.json',()=>tools.mcp__codex_apps__library_replace_library_file(args));publication=r.structuredContent;return r;},
      mcp__codex_apps__library_prepare_materialize:async args=>{live();counts.libraryCalls++;return await call('caller-library-materialize.original.json',()=>tools.mcp__codex_apps__library_prepare_materialize(args));}}
  };
}
