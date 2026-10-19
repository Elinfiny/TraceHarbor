export async function bridge118(frame, state, tools) {
  const canonical = v => v === null || typeof v !== 'object' ? JSON.stringify(v) : Array.isArray(v) ? '[' + v.map(canonical).join(',') + ']' : '{' + Object.keys(v).sort().map(k => JSON.stringify(k) + ':' + canonical(v[k])).join(',') + '}';
  const same = (a, b) => canonical(a) === canonical(b);
  const capture = async (name, value) => {
    const raw = JSON.stringify(value);
    if (raw.length > 2097152) throw Error('Original exceeds bounded capture; UNKNOWN');
    const path = state.capture_directory + '/' + frame.seq + '.' + name + '.json';
    return await tools.apply_patch('*** Begin Patch\n*** Add File: ' + path + '\n+' + raw.split('\n').join('\n+') + '\n*** End Patch');
  };
  if (state.failed || state.pending || frame.schema !== 'TRACE118_HOST_REQUEST' || frame.seq !== state.next_seq || !same(frame.context, state.context) || frame.deadline_utc_ms > state.deadline_utc_ms || frame.deadline_utc_ms !== state.actual_phase_deadline_utc_ms || frame.request_digest !== state.expected_request_digest || !same({op:frame.op,args:frame.args},state.expected_operation)) throw Error('Exact holder/source/sequence/planned operation required');
  if (Date.now() >= Math.min(state.deadline_utc_ms,frame.deadline_utc_ms)) throw Error('Request expired before tool');
  if (!/^\/workspace\/[A-Za-z0-9_\-/]+$/.test(state.capture_directory) || state.capture_directory.includes('..')) throw Error('Trusted private capture root required');
  await capture('request-before-tool', frame);
  state.pending = true;
  const a = frame.args;
  const repo = 'Elinfiny/TraceHarbor';
  const writes = ['github_create_blob','github_create_tree','github_create_commit','github_create_ref','library_replace'];
  if (writes.includes(frame.op) && (state.read_only !== false || state.consumed_effect_digest !== frame.request_digest)) {state.failed = true;throw Error('Read-only or missing exact originalwriter consumed intent');}
  if (writes.includes(frame.op)) {state.consumed_effect_digest = null;await capture('consumed-before-native-effect', {seq:frame.seq,request_digest:frame.request_digest,status:'ATTEMPTING_NO_RETRY'});}
  let original = null, transport_error = null;
  try {
    switch (frame.op) {
      case 'github_fetch':
        if (!state.allowed_fetch_urls.includes(a.url)) throw Error('Exact source-bound GET allowlist');
        original = await tools.mcp__codex_apps__github_fetch({url:a.url}); break;
      case 'github_create_blob':
        if (a.repository_full_name !== repo || !['utf-8','base64'].includes(a.encoding) || typeof a.content !== 'string' || a.content.length > 190000) throw Error('Bounded exact blob');
        original = await tools.mcp__codex_apps__github_create_blob(a); break;
      case 'github_create_tree':
        if (a.repository_full_name !== repo || a.base_tree_sha !== state.source_tree || !Array.isArray(a.tree_elements) || a.tree_elements.length !== 1 || a.tree_elements[0].mode !== '100644' || a.tree_elements[0].type !== 'blob' || a.tree_elements[0].sha !== state.last_blob_sha) throw Error('Exact preceding returned blob/tree');
        original = await tools.mcp__codex_apps__github_create_tree(a); break;
      case 'github_create_commit':
        if (a.repository_full_name !== repo || a.parent_sha !== state.context.source_sha || a.tree_sha !== state.last_tree_sha || a.additional_parent_shas?.length) throw Error('Exact source soleparent and preceding tree');
        original = await tools.mcp__codex_apps__github_create_commit(a); break;
      case 'github_create_ref':
        if (a.repository_full_name !== repo || a.sha !== state.last_commit_sha || !/^traceharbor-(counter116-(admit|consumed)-[a-f0-9]{64}|encrypted104-[a-f0-9]{32})$/.test(a.branch_name) || Object.keys(a).some(k => !['repository_full_name','branch_name','sha'].includes(k))) throw Error('Exact create-only once branch');
        // Logical historical create_ref maps to the ACTUAL create-only tool.
        original = await tools.mcp__codex_apps__github_create_branch({repository_full_name:repo,branch_name:a.branch_name,sha:a.sha}); break;
      case 'github_fetch_workflow_run_artifacts':
        if (a.repo_full_name !== repo || a.run_id !== state.context.run_id || a.name !== 'traceharbor-recipient104-' + a.run_id + '-1') throw Error('Exact current run artifact');
        original = await tools.mcp__codex_apps__github_fetch_workflow_run_artifacts(a); break;
      case 'github_download_workflow_artifact':
        if (a.repo_full_name !== repo || a.artifact_id !== state.verified_artifact_id || a.file_name !== 'recipient118.zip') throw Error('Previously verified current artifact ID');
        original = await tools.mcp__codex_apps__github_download_workflow_artifact(a); break;
      case 'library_replace':
        if (a.library_file_id !== 'libfile_3ee8270f03d8819188e1de1f75c3d824' || a.expected_current_version !== state.actual_own_version || a.file !== state.verified_writer_candidate) throw Error('Actual originalwriter candidate/current CAS required');
        original = await tools.mcp__codex_apps__library_replace_library_file(a); break;
      case 'library_materialize':
        if (!same(a.items,state.verified_materialize_items) || a.destination.directory !== state.verified_materialize_directory) throw Error('Actual pinned returned reference required');
        original = await tools.mcp__codex_apps__library_prepare_materialize(a); break;
      default: throw Error('Unsupported tool; no arbitrary invocation/HTTP/eval');
    }
  } catch (error) {transport_error = {exception_class:error?.name || 'Error',status:'UNKNOWN_NO_RETRY'};}
  // Native tool result/exception is persisted BEFORE parsing or deadline guards.
  await capture('native-tool-original', {original_result:original,transport_error});
  const late = Date.now() >= Math.min(state.deadline_utc_ms,frame.deadline_utc_ms);
  if (!late && !transport_error && !original?.isError) {
    const returned = original?.structuredContent;
    if (frame.op === 'github_create_blob') state.last_blob_sha = returned?.sha;
    if (frame.op === 'github_create_tree') state.last_tree_sha = returned?.sha;
    if (frame.op === 'github_create_commit') state.last_commit_sha = returned?.sha;
  }
  const response = {schema:'TRACE118_HOST_RETURN',seq:frame.seq,context:frame.context,op:frame.op,request_digest:frame.request_digest,original_result:original,transport_error,late};
  await capture('response-before-normalization', response);
  if (late || transport_error || original?.isError) state.failed = true;
  state.pending = false;
  state.next_seq += 1;
  // An actual native terminal is returned to this SAME existing holder.
  const terminal = await tools.write_stdin({session_id:state.holder_session_id,chars:JSON.stringify(response)+'\n',yield_time_ms:1000,max_output_tokens:2000});
  await capture('same-holder-native-return', terminal);
  return {seq:frame.seq,late,transport_error,original_is_error:original?.isError === true,holder_terminal:terminal,native_authority:false};
}
