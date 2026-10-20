export async function runAdminDispatcher123(bundle, bridge118, native) {
  // Existing native primitives only. This source is preloaded before launch;
  // no per-frame model turn, new HTTP executor, eval, import or tool factory.
  const canonical = v => v === null || typeof v !== 'object' ? JSON.stringify(v) : Array.isArray(v) ? '[' + v.map(canonical).join(',') + ']' : '{' + Object.keys(v).sort().map(k => JSON.stringify(k) + ':' + canonical(v[k])).join(',') + '}';
  const same = (a,b) => canonical(a) === canonical(b);
  if (!['ADMIN123','SYNTHETIC_SOURCE_ONLY'].includes(native.mode) || bundle.mode !== native.mode || bundle.frames !== 2 || bundle.actual_current_version !== 437 || bundle.next_version !== 438 || bundle.context.direction_number !== 123 || bundle.context.domain !== 'NECESSARY_CURRENT123_SOURCE_FREEZE' || bundle.context.run_id !== null || bundle.context.once_receipt_sha256 !== null) throw Error('Exact current administrative scope, never a native capability');
  const state = {context:bundle.context,deadline_utc_ms:bundle.deadline_utc_ms,next_seq:1,pending:false,failed:false,read_only:false,capture_directory:bundle.capture_directory,source_tree:bundle.source_tree,allowed_fetch_urls:[]};
  const metrics = {launches:0,frames:0,writes:0,polls:0,guards:0,model_turns_between_frames:0,native_authority:false};
  const started = native.now();
  if (started >= bundle.deadline_utc_ms || bundle.deadline_utc_ms-started > 180000) throw Error('Immutable admin parent at most180s; no clock reset');
  let terminal = await native.launch(); metrics.launches++;
  await native.save('holder-start.original.json',terminal);
  if (!Number.isInteger(terminal.session_id) || terminal.exit_code != null) throw Error('Actual ONE live directPTY holder required');
  state.holder_session_id = terminal.session_id;
  let pendingText = '';
  const frameFrom = async seq => {
    while (true) {
      if (native.now() >= bundle.deadline_utc_ms) throw Error('Original admin parent expired; no extra poll');
      pendingText += terminal.output || '';
      const lines = pendingText.split('\n').map(x=>x.trim()).filter(Boolean);
      if (lines.length) {
        if (lines.length !== 1) throw Error('Exact one bounded original frame, no mixed output');
        if (lines[0].length > 1048576) throw Error('Frame cap');
        let frame; try {frame=JSON.parse(lines[0]);} catch {throw Error('Malformed original frame; no dependent effect');}
        if (frame.schema !== 'TRACE118_HOST_REQUEST' || frame.seq !== seq || !same(frame.context,bundle.context) || !Number.isSafeInteger(frame.deadline_utc_ms) || frame.deadline_utc_ms > bundle.deadline_utc_ms || native.now() >= frame.deadline_utc_ms || !/^[a-f0-9]{64}$/.test(frame.request_digest)) throw Error('Exact source/context/order/current deadline');
        pendingText=''; return frame;
      }
      if (terminal.exit_code != null || metrics.polls >= 6 || metrics.writes >= 8) throw Error('No frame/closed holder; finite no-retry');
      terminal=await native.poll(state.holder_session_id);metrics.polls++;metrics.writes++;
      await native.save('poll'+metrics.polls+'.original.json',terminal);
    }
  };
  let publication = null;
  const stages=[];
  for (let seq=1;seq<=2;seq++) {
    const frame=await frameFrom(seq);
    const expected=seq===1 ? {op:'library_replace',args:{library_file_id:bundle.own_library_file_id,file:bundle.upload_path,expected_current_version:437,version_reason:'CURRENT scoped source-pinned original producer binding; necessary planned PUBLISH_INTENT; no UNKNOWN retry'}} : {op:'library_materialize',args:{items:[{library_file_id:bundle.own_library_file_id,file_id:publication.file_id,file_name:publication.file_name}],destination:{directory:bundle.readback_directory}}};
    if (!same({op:frame.op,args:frame.args},expected)) throw Error('Closed two-operation administrative plan only');
    // Actual guarded source verifies original private writer terminal/output,
    // config/source/current-own binding and saved request digest before effect.
    const guarded = await native.verify(seq); metrics.guards++;
    await native.save('guard'+seq+'.native-original.json',guarded);
    if (guarded.exit_code !== 0) throw Error('Original producer/pre-effect guard not terminal0');
    let ticket;try {ticket=JSON.parse(guarded.output);} catch {throw Error('Complete actual guard output required');}
    const scope=native.mode==='ADMIN123'?'ACTUAL_ADMIN123_GUARD':'SYNTHETIC_SOURCE_ONLY';
    if (ticket.scope !== scope || ticket.seq !== seq || ticket.request_digest !== frame.request_digest || !same(ticket.context,bundle.context) || ticket.current_writer_sha256 !== bundle.writer_sha256 || ticket.config_sha256 !== bundle.config_sha256 || ticket.native_authority !== false) throw Error('Fixture/cross-source/serialized authority refused');
    state.expected_request_digest=frame.request_digest;state.expected_operation=expected;state.actual_phase_deadline_utc_ms=frame.deadline_utc_ms;
    if (seq===1) {state.actual_own_version=437;state.verified_writer_candidate=bundle.upload_path;state.consumed_effect_digest=frame.request_digest;}
    else {state.verified_materialize_items=expected.args.items;state.verified_materialize_directory=bundle.readback_directory;}
    const before=native.now();
    const result=await bridge118(frame,state,native.tools);metrics.frames++;metrics.writes++;
    stages.push({seq,before_utc_ms:before,after_utc_ms:native.now(),duration_ms:native.now()-before});
    if (result.late || result.transport_error || result.original_is_error || state.failed) throw Error('First UNKNOWN retained; no follow-on');
    terminal=result.holder_terminal;
    if (seq===1) {
      publication=await native.publicationOriginal();
      if (publication.status !== 'succeeded' || publication.library_file_id !== bundle.own_library_file_id || publication.current_version_number !== 438 || typeof publication.file_id !== 'string' || typeof publication.file_name !== 'string') throw Error('Exact preceding native CAS438 return required');
    }
  }
  // Normal source holder executes its own allattrs/readback guards before exit.
  while (terminal.exit_code == null) {
    if (native.now() >= bundle.deadline_utc_ms || metrics.polls>=6 || metrics.writes>=8) throw Error('No authentic terminal within original admin bounds');
    terminal=await native.poll(state.holder_session_id);metrics.polls++;metrics.writes++;
    await native.save('poll'+metrics.polls+'.original.json',terminal);
  }
  if (terminal.exit_code!==0 || metrics.frames!==2 || native.now()>=bundle.deadline_utc_ms) throw Error('Same holder authentic terminal0 required');
  const finalLines=(terminal.output||'').split('\n').map(x=>x.trim()).filter(Boolean);let final;
  try {final=JSON.parse(finalLines[finalLines.length-1]);} catch {throw Error('Actual holder terminal projection required');}
  if (final.schema!=='TRACE120_HOLDER_TERMINAL' || final.result!=='PASS' || final.exit_code!==0) throw Error('Source holder semantic closure');
  const proof={schema:'TRACE123_PRELOADED_ADMIN_DISPATCHER',scope:native.mode,holder_session_id:state.holder_session_id,metrics,stages,started_utc_ms:started,ended_utc_ms:native.now(),original_parent_deadline_utc_ms:bundle.deadline_utc_ms,terminal,publication,native_authority:false};
  await native.save('dispatcher123-proof.json',proof);
  return proof;
}
