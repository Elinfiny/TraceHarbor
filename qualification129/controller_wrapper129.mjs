// Exact source compile, no global polyfill, seal replacement or native call.
export function compileController129(source,actualTools){
 if(typeof source!=='string'||typeof actualTools!=='object'||actualTools===null||/^\s*import\s/m.test(source))throw Error('Pinned standalone caller and actual lexical tools required');
 const removed=(source.match(/^export /gm)||[]).length;
 const transformed=source.replace(/^export /gm,'');
 const suffix='\nreturn Object.freeze({snapshotPlain129,utf8ByteCount129,CONFIG_LIMITS129,prepare127,counts127,collectPreflight128,PREFLIGHT128});';
 const result=new Function('tools',transformed+suffix)(actualTools);
 return {api:result,transformation:{schema:'REMOVE_TOP_LEVEL_ESM_EXPORT_PREFIX_ONLY_V1',removed_prefixes:removed,source_characters:source.length,body_substitution:false,global_polyfill:false,native_factory_invoked:false,lexical_tools:'ACTUAL_ORIGINAL_TOOLS_OBJECT'}};
}
