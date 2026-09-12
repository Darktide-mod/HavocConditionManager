"""Real package I/O, frozen mission scripts and fresh next-mission Lua loading.

Only an isolated build/checks directory is used as APPDATA. The template
provider is a disk-backed Lua fixture; it is not an emulation of DMF itself.
"""
from project_env import PROJECT, CHECKS
from pathlib import Path
import os
import tempfile

from lupa.luajit21 import LuaRuntime


def run(directory):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute("""
        Mods={lua={ffi=require('ffi'),loadstring=loadstring,debug=debug}}
        table.clear=function(t)for k in pairs(t)do t[k]=nil end end
    """)
    source = PROJECT / 'src/HavocConditionManager/scripts/mods/HavocConditionManager/diy'
    for alias, name in (
        ('S', 'schema'), ('C', 'codec'), ('K', 'catalog'), ('E', 'engine'),
        ('P', 'packages'), ('H', 'sha256'), ('F', 'files'), ('B', 'library'),
        ('PL', 'package_library'), ('Scripts', 'scripts'),
    ):
        lua.globals()[alias] = lua.execute((source / f'diy_{name}.lua').read_text(encoding='utf-8'))
    lua.globals().template_path = (directory / 'bundled-templates.lua').as_posix()
    lua.execute(r'''
        A=P.new(S,C,H)
        function make_package(id)
            local document=assert(S.validate({format=S.format,version=1,kind='conditions',id=id,name=id,
                entries={{id='effect',name=id,description='Reload test',script=true,
                    targets={kind='minions'}}}},K,'conditions'))
            local files=A.from_document(document,id,true)
            local manifest=assert(C.decode(files['package.json']))
            manifest.version=2
            manifest.package_version='1.0.0'
            manifest.files[#manifest.files+1]='lua/helper.lua'
            files['package.json']=assert(C.encode(manifest))
            return files
        end
        consumer=make_package('reload-consumer')
        consumer['lua/main.lua']=[[
            private_loads=(private_loads or 0)+1
            assert(private_loads==1,'Every mission must have a fresh package environment')
            local extra=0.1
            local helper=package_require('lua/helper.lua')
            local dependency=dependency_require('reload-dependency')
            local value=extra+helper+dependency.value
            return {api_version={major=1,minor=0},entries={effect={interval=.1,
                on_activate=function(ctx)
                    ctx:set_effects({stats={damage=value}})
                    ctx:on_cleanup(function(reason)ctx:log('cleanup:'..reason)end)
                end,
                on_update=function(ctx)ctx:set_effects({stats={damage=value}})end
            }}}
        ]]
        consumer['lua/helper.lua']='return 0.2'
        local manifest=assert(C.decode(consumer['package.json']))
        manifest.dependencies={{id='reload-dependency',min_version='1.0.0'}}
        consumer['package.json']=assert(C.encode(manifest))
        dependency=make_package('reload-dependency')
        dependency['lua/main.lua']=[[
            local helper=package_require('lua/helper.lua')
            return {api_version={major=1,minor=0},exports={value=helper},entries={effect={}}}
        ]]
        dependency['lua/helper.lua']='return 0.3'
        for id,files in pairs({['reload-consumer']=consumer,['reload-dependency']=dependency})do
            assert(A.validate(files,K,'conditions',id))
        end
        assert(private_loads==nil,'Scanning may compile but must not execute package Lua')

        fs=assert(F.new(require('ffi'),'HavocConditionManager'))
        assert(fs.write_package('reload-consumer',consumer,P.id,P.path))
        assert(fs.write_package('reload-dependency',dependency,P.id,P.path))
        settings={};busy=false;changes={};template_loads=0;cleanup_log={};errors={};cache_clears=0
        mod={get=function(_,key)return settings[key]end,
            set=function(_,key,value)settings[key]=S.copy(value)end,
            localize=function(_,key)return key end}
        get_mod=function()return nil end
        library=PL.new(mod,'conditions',K,S,C,F,B,P,H,{
            name='HavocConditionManager',busy=function()return busy end,
            changed=function(reason)changes[#changes+1]=reason end,
            before_reload=function()cache_clears=cache_clears+1 end,
            templates=function()
                assert(cache_clears>0,'Clear caches before reading the template provider')
                template_loads=template_loads+1
                return dofile(template_path)
            end})
        assert(not library.last_error and #library.files==2 and template_loads==0)
        id=A.identity('reload-consumer','effect')
        assert(library.set_options({enabled=true,selected={id}}))
        unit={id='test-minion',kind='minions'}
        native={key=function(u)return u.id end,info=function(u)return u end,
            alive=function(u)return u~=nil end,context=function()return {}end,
            units=function()return {unit}end,action=function()return true end,
            error=function(message)errors[#errors+1]=tostring(message)end}
        function start(snapshot)
            local engine=Scripts.attach(E.new(snapshot.document,K,native,123),snapshot,
                {Schema=S,Packages=P,PackageAPI=A,Engine=E,native=native,catalog=K,
                    log=function(_,message)cleanup_log[#cleanup_log+1]=message end})
            engine.set_global(E.choose(snapshot.document,snapshot.options,123))
            return engine
        end
        function expect(engine,value)
            engine.tick(.11)
            assert(math.abs((engine.effects(unit).stats.damage or 0)-value)<.000001,
                'Engine executed the wrong package generation')
            assert(#errors==0,table.concat(errors,'\n'))
        end
        frozen=library.snapshot();old_engine=start(frozen);expect(old_engine,.6)
        local unchanged=library.signature();local callbacks=#changes
        local old_document=library.document
        library.document.entries[1].description='stale parsed value'
        assert(library.scan() and library.signature()==unchanged and #changes==callbacks)
        assert(cache_clears==1 and library.document~=old_document and library.document.entries[1].description~='stale parsed value')
        assert(library.snapshot()~=frozen,'Even same-content refresh must discard the cached snapshot')
        assert(#cleanup_log==0,'Even a no-change refresh must not finish the active engine')

        -- Change both the entrypoint and a local module without a version bump.
        consumer['lua/main.lua']=consumer['lua/main.lua']:gsub('local extra=0.1','local extra=0.2')
        consumer['lua/helper.lua']='return 0.4'
        assert(fs.write_package('reload-consumer',consumer,P.id,P.path,true))
        busy=true
        assert(not library.set_options({selected={}}),'Mission selections remain locked')
        assert(library.scan(),'Package discovery remains available during a mission')
        assert(library.signature()~=unchanged and changes[#changes]=='packages')
        assert(library.packages['reload-consumer'].manifest.package_version=='1.0.0')
        assert(frozen.packages['reload-consumer'].files['lua/helper.lua']=='return 0.2')
        assert(library.snapshot().packages['reload-consumer'].files['lua/helper.lua']=='return 0.4')
        expect(old_engine,.6)
        assert(#cleanup_log==0,'Refresh must retain current effects and cleanup callbacks')
        old_engine.finish();old_engine.finish()
        assert(#cleanup_log==1 and cleanup_log[1]=='cleanup:mission_end')
        assert(next(old_engine.package_sources)==nil,'Finished engines release source/module generations')
        next_snapshot=library.snapshot();next_engine=start(next_snapshot);expect(next_engine,.9)

        -- Dependency-only Lua changes must invalidate the consuming package closure.
        local consumer_hash=library.packages['reload-consumer'].hash
        local entry_hash=library.entry_hashes[id];local signature=library.signature()
        dependency['lua/helper.lua']='return 0.8'
        assert(fs.write_package('reload-dependency',dependency,P.id,P.path,true))
        assert(library.scan() and library.signature()~=signature)
        assert(library.packages['reload-consumer'].hash==consumer_hash)
        assert(library.entry_hashes[id]~=entry_hash,'Dependency contents affect consumer identity')
        assert(library.packages['reload-dependency'].manifest.package_version=='1.0.0')
        assert(next_snapshot.packages['reload-dependency'].files['lua/helper.lua']=='return 0.3')
        expect(next_engine,.9);assert(#cleanup_log==1)
        next_engine.finish()
        dependency_engine=start(library.snapshot());expect(dependency_engine,1.4)

        -- Each explicit extraction reads the current bundled-template provider.
        function write_template_provider()
            local file=assert(io.open(template_path,'wb'))
            file:write('return {\n')
            for package_id,files in pairs({['reload-consumer']=consumer,['reload-dependency']=dependency})do
                file:write(string.format('[%q]={\n',package_id))
                for path,text in pairs(files)do file:write(string.format('[%q]=%q,\n',path,text))end
                file:write('},\n')
            end
            file:write('}\n');file:close()
        end
        write_template_provider()
        assert(library.extract_templates() and template_loads==1)
        consumer['lua/helper.lua']='return 0.6'
        write_template_provider()
        assert(library.extract_templates() and template_loads==2)
        assert(fs.read_package('reload-consumer',P.id,P.path)['lua/helper.lua']=='return 0.6')
        assert(library.snapshot().packages['reload-consumer'].files['lua/helper.lua']=='return 0.6')
        assert(library.options.selected[1]==id and library.options.enabled)
        expect(dependency_engine,1.4);assert(#cleanup_log==2)
        dependency_engine.finish()
        template_engine=start(library.snapshot());expect(template_engine,1.6)
        template_engine.finish();assert(#cleanup_log==4 and #errors==0)
        assert(private_loads==nil,'Fresh package environments never leak into native globals')
    ''')
    package_directory = Path(lua.globals().library.directory()[0]).resolve()
    assert package_directory.is_relative_to(directory.resolve())
    assert list((package_directory.parent / 'package-backups').iterdir())


previous_appdata = os.environ.get('APPDATA')
try:
    with tempfile.TemporaryDirectory(prefix='diy-package-reload-', dir=CHECKS) as isolated:
        isolated = Path(isolated)
        os.environ['APPDATA'] = str(isolated)
        (isolated / 'Fatshark/Darktide').mkdir(parents=True)
        run(isolated)
finally:
    if previous_appdata is None:
        os.environ.pop('APPDATA', None)
    else:
        os.environ['APPDATA'] = previous_appdata

print('HCM package refresh: real file and dependency reload without version bumps; '
      'active-mission snapshots preserved; fresh next-mission Lua and cleanup; '
      'repeated template-provider extraction: PASS')
