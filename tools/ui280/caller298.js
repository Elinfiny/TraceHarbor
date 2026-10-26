// Authenticated connector caller, not a JSON provenance flag or a Git publisher.
// api.read MUST be the actual supported Library tool binding supplied by host.
async function preparePublication298(api, pins, sourceTree, adoptionSelector, sha256, sealCheck) {
  async function current(stable) {
    const first=await api.read({read:[{ref_id:stable,mode:'full',max_lines:1000}]});
    await api.retainOriginal(first);const one=first.structuredContent.results[0], rows=[one];
    for(let line=1001;line<=one.total_lines;line+=1000) {
      const ret=await api.read({read:[{ref_id:stable,mode:'full',start_line:line,max_lines:1000}]});
      await api.retainOriginal(ret);const next=ret.structuredContent.results[0];
      if(next.version_id!==one.version_id||next.file_id!==one.file_id)throw Error('PROVIDER_VERSION_DRIFT'); rows.push(next);
    }
    const raw=rows.map(x=>x.content.join('\n')).join('\n');
    const length=x=>unescape(encodeURIComponent(x)).length;const bytes=length(raw)===one.size_bytes?raw:length(raw+'\n')===one.size_bytes?raw+'\n':null;if(bytes===null)throw Error('FULLBYTE_COUNT'); // exact UTF8 with/without terminalLF, never canonicalized
    const object=JSON.parse(bytes);await sealCheck(object);
    return {stable,version:Number(one.version_id),file_id:one.file_id,bytes:one.size_bytes,raw_sha256:await sha256(bytes),self_sha256:object.self_sha256,object};
  }
  const master=await current('libfile_f67b07d0a4288191b60f3469d264f99c');
  const auditor=await current('libfile_779cb59e1cd08191a438c5537497f60d');
  const policy=await current('libfile_6f69ae483b088191a1fffefca617bbd5');
  const canonical=x=>JSON.stringify(x,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,v[k]])):v);const vector=await sha256(canonical(pins));
  const review=adoptionSelector.split('/').reduce((v,k)=>v?.[k],auditor.object);
  const once=master.object.native298_publication_once;
  if(!review||review.source_vector_sha256!==vector||review.state!=='ADOPTED_EXACT_SOURCE_ONLY')throw Error('ACTUAL_CURRENT_ADOPTION_MISSING');
  if(!once||once.state!=='RESERVED'||once.source_vector_sha256!==vector||once.source_tree!==sourceTree||once.policy_raw_sha256!==policy.raw_sha256)throw Error('ACTUAL_MASTER_ONCE_CAS_MISSING');
  // No CAS here: actual provider CAS/readback reservation precedes these reads.
  // Never relabel compact bytes as the historical giant Auditor anchor.
  delete master.object;delete auditor.object;delete policy.object;
  if(!/^[0-9a-f]{40}$/.test(sourceTree))throw Error('EXACT_SOURCE_TREE');return {schema:'TRACE298_PREPUBLICATION_V1',state:'ADMITTED_ONCE',source:'__NATIVE_CHECKOUT__',parent:'7fc30e33c753b5335b1492a74eb09889d83b479d',tree:sourceTree,source_pins:pins,evidence:{master:{...master,source_vector_sha256:vector,once_state:'RESERVED'},auditor_identity_anchor:'libfile_f87a6a307f70819194e0af0fa453afd1',auditor_current:{...auditor,source_vector_sha256:vector,review_selector:adoptionSelector,body_sha256:await sha256(canonical(review))},policy},effect_id:once.effect_id,budget:once.budget,free_existing_host:once.free_existing_host,sandbox_required:true};
}
