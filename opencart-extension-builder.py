# ~*~ coding:utf-8 ~*~
import os, sys, getopt

directoryStructure = {"admin":["controller", "language", "model", 'view'],
                      "catalog":["controller", "language", "model", "view"]}

fileContents = {"admin_language": '''<?php
// Heading
$_['heading_title']    = '{CCModuleName}';

// Text
$_['text_module']      = 'Modules';
$_['text_success']     = 'Success: You have modified {SSModuleName} module!';
$_['text_edit']        = 'Edit {CCModuleName} Module';

// Entry
$_['entry_admin']      = 'Admin Users Only';
$_['entry_status']     = 'Status';

// Error
$_['error_permission'] = 'Warning: You do not have permission to modify {SSModuleName} module!';
''',

"admin_controller": '''<?php
class ControllerModule{CCModuleName} extends Controller {
    private $error = array();

    public function install(){
        //install script goes here
    }

    public function uninstall(){
        //uninstall script goes here
    }
    
    public function index() {
        $this->load->language('module/{SSModuleName}');

        $this->document->setTitle($this->language->get('heading_title'));

        $this->load->model('setting/setting');

        if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validate()) {
            $this->model_setting_setting->editSetting('{SSModuleName}', $this->request->post);

            $this->session->data['success'] = $this->language->get('text_success');

            $this->response->redirect($this->url->link('extension/module', 'token=' . $this->session->data['token'], 'SSL'));
        }

        $data['heading_title'] = $this->language->get('heading_title');

        $data['text_edit'] = $this->language->get('text_edit');
        $data['text_yes'] = $this->language->get('text_yes');
        $data['text_no'] = $this->language->get('text_no');
        $data['text_enabled'] = $this->language->get('text_enabled');
        $data['text_disabled'] = $this->language->get('text_disabled');

        $data['entry_admin'] = $this->language->get('entry_admin');
        $data['entry_status'] = $this->language->get('entry_status');

        $data['button_save'] = $this->language->get('button_save');
        $data['button_cancel'] = $this->language->get('button_cancel');

        if (isset($this->error['warning'])) {
            $data['error_warning'] = $this->error['warning'];
        } else {
            $data['error_warning'] = '';
        }

        $data['breadcrumbs'] = array();

        $data['breadcrumbs'][] = array(
            'text' => $this->language->get('text_home'),
            'href' => $this->url->link('common/dashboard', 'token=' . $this->session->data['token'], 'SSL')
        );

        $data['breadcrumbs'][] = array(
            'text' => $this->language->get('text_module'),
            'href' => $this->url->link('extension/module', 'token=' . $this->session->data['token'], 'SSL')
        );

        $data['breadcrumbs'][] = array(
            'text' => $this->language->get('heading_title'),
            'href' => $this->url->link('module/{SSModuleName}', 'token=' . $this->session->data['token'], 'SSL')
        );

        $data['action'] = $this->url->link('module/{SSModuleName}', 'token=' . $this->session->data['token'], 'SSL');

        $data['cancel'] = $this->url->link('extension/module', 'token=' . $this->session->data['token'], 'SSL');

        if (isset($this->request->post['{SSModuleName}_admin'])) {
            $data['{SSModuleName}_admin'] = $this->request->post['{SSModuleName}_admin'];
        } else {
            $data['{SSModuleName}_admin'] = $this->config->get('{SSModuleName}_admin');
        }

        if (isset($this->request->post['{SSModuleName}_status'])) {
            $data['{SSModuleName}_status'] = $this->request->post['{SSModuleName}_status'];
        } else {
            $data['{SSModuleName}_status'] = $this->config->get('{SSModuleName}_status');
        }

        $data['header'] = $this->load->controller('common/header');
        $data['column_left'] = $this->load->controller('common/column_left');
        $data['footer'] = $this->load->controller('common/footer');

        $this->response->setOutput($this->load->view('module/{SSModuleName}.tpl', $data));
    }

    protected function validate() {
        if (!$this->user->hasPermission('modify', 'module/{SSModuleName}')) {
            $this->error['warning'] = $this->language->get('error_permission');
        }

        return !$this->error;
    }
}
''',

"admin_model":'''<?php class ModelModule{CCModuleName}{
    public function install(){
        //install script goes here
    }

    public function uninstall(){
        //uninstall script goes here
    }
}
''',

"admin_view": '''<?php echo $header; ?><?php echo $column_left; ?>
<div id="content">
    <div class="page-header">
        <div class="container-fluid">
            <div class="pull-right">
                <button type="submit" form="form-{SSModuleName}" data-toggle="tooltip" title="<?php echo $button_save; ?>" class="btn btn-primary"><i class="fa fa-save"></i></button>
                <a href="<?php echo $cancel; ?>" data-toggle="tooltip" title="<?php echo $button_cancel; ?>" class="btn btn-default"><i class="fa fa-reply"></i></a></div>
            <h1><?php echo $heading_title; ?></h1>
            <ul class="breadcrumb">
                <?php foreach ($breadcrumbs as $breadcrumb) { ?>
                <li><a href="<?php echo $breadcrumb['href']; ?>"><?php echo $breadcrumb['text']; ?></a></li>
                <?php } ?>
            </ul>
        </div>
    </div>
    <div class="container-fluid">
        <?php if ($error_warning) { ?>
            <div class="alert alert-danger"><i class="fa fa-exclamation-circle"></i> <?php echo $error_warning; ?>
                <button type="button" class="close" data-dismiss="alert">&times;</button>
            </div>
        <?php } ?>
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title"><i class="fa fa-pencil"></i> <?php echo $text_edit; ?></h3>
            </div>
            <div class="panel-body">
                <form action="<?php echo $action; ?>" method="post" enctype="multipart/form-data" id="form-{SSModuleName}" class="form-horizontal">
                    <div class="form-group">
                        <label class="col-sm-2 control-label"><?php echo $entry_admin; ?></label>
                        <div class="col-sm-10">
                            <label class="radio-inline">
                                <?php if (${SSModuleName}_admin) { ?>
                                    <input type="radio" name="{SSModuleName}_admin" value="1" checked="checked" />
                                    <?php echo $text_yes; ?>
                                <?php } else { ?>
                                    <input type="radio" name="{SSModuleName}_admin" value="1" />
                                    <?php echo $text_yes; ?>
                                <?php } ?>
                            </label>
                            <label class="radio-inline">
                                <?php if (!${SSModuleName}_admin) { ?>
                                    <input type="radio" name="{SSModuleName}_admin" value="0" checked="checked" />
                                    <?php echo $text_no; ?>
                                <?php } else { ?>
                                    <input type="radio" name="{SSModuleName}_admin" value="0" />
                                    <?php echo $text_no; ?>
                                <?php } ?>
                            </label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-2 control-label" for="input-status"><?php echo $entry_status; ?></label>
                        <div class="col-sm-10">
                            <select name="{SSModuleName}_status" id="input-status" class="form-control">
                            <?php if (${SSModuleName}_status) { ?>
                                <option value="1" selected="selected"><?php echo $text_enabled; ?></option>
                                <option value="0"><?php echo $text_disabled; ?></option>
                            <?php } else { ?>
                                <option value="1"><?php echo $text_enabled; ?></option>
                                <option value="0" selected="selected"><?php echo $text_disabled; ?></option>
                            <?php } ?>
                            </select>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
<?php echo $footer; ?>
''',

"catalog_controller": '''<?php
class ControllerModule{CCModuleName} extends Controller {
    public function index() {
        $status = true;

        if ($this->config->get('{SSModuleName}_admin')) {
            $this->load->library('user');

            $this->user = new User($this->registry);

            $status = $this->user->isLogged();
        }

        if ($status) {
            $this->load->language('module/{SSModuleName}');

            $data['heading_title'] = $this->language->get('heading_title');

            $data['text_{SSModuleName}'] = $this->language->get('text_{SSModuleName}');

            $data['{SSModuleName}_id'] = $this->config->get('config_{SSModuleName}_id');

            $data['{SSModuleName}s'] = array();

            $data['{SSModuleName}s'][] = array(
                '{SSModuleName}_id' => 0,
                'name'     => $this->language->get('text_default'),
                'url'      => HTTP_SERVER . 'index.php?route=common/home&session_id=' . $this->session->getId()
            );

            $this->load->model('setting/{SSModuleName}');

            $results = [];

            $data['{SSModuleName}s'] = $results;

            if (file_exists(DIR_TEMPLATE . $this->config->get('config_template') . '/template/module/{SSModuleName}.tpl')) {
                return $this->load->view($this->config->get('config_template') . '/template/module/{SSModuleName}.tpl', $data);
            } else {
                return $this->load->view('default/template/module/{SSModuleName}.tpl', $data);
            }
        }
    }
}
''',

"catalog_language": '''<?php
// Heading
$_['heading_title'] = '{CCModuleName}';

// Text
$_['text_default']  = 'Default';
$_['text_{SSModuleName}']    = 'Select One.';
''',

"catalog_model": '''<?php
class ModelModule{CCModuleName} extends Model {

}
''',

"catalog_view": '''<div class="panel panel-default">
    <div class="panel-heading"><?php echo $heading_title; ?></div>
        <p style="text-align: center;"><?php echo $text_{SSModuleName}; ?></p>
        <?php foreach (${SSModuleName}s as ${SSModuleName}) { ?>
            <?php if (${SSModuleName}['{SSModuleName}_id'] == ${SSModuleName}_id) { ?>
                <a href="<?php echo ${SSModuleName}['url']; ?>"><b><?php echo ${SSModuleName}['name']; ?></b></a><br />
            <?php } else { ?>
                <a href="<?php echo ${SSModuleName}['url']; ?>"><?php echo ${SSModuleName}['name']; ?></a><br />
        <?php } ?>
    <?php } ?>
    <br />
</div>
'''
}

def getContent(contentIndex, moduleName):
    camelCasedModuleName = ''
    arrModuleName = moduleName.split('_')
    for i in arrModuleName:
        camelCasedModuleName += i[0].upper() + i[1:]

    smallModuleName = moduleName.lower()
    return fileContents[contentIndex].replace('{SSModuleName}', smallModuleName).replace('{CCModuleName}', camelCasedModuleName)

def createDirectories(path, moduleName, adminonly):
    if '' != path:
        error = False
        currentdir = os.path.dirname(os.path.realpath(__file__))
        currentPath = ''

        if os.path.exists(os.path.join(currentdir, path)):
            currentPath = os.path.join(currentdir, path)
        elif os.path.exists(path):
            currentPath = path
        else:
            error = True

        if not error:
            for i in directoryStructure:
                if 'admin' != i:
                    continue

                if os.path.exists(os.path.join(currentPath, i)):
                    if type(directoryStructure[i]) is list:
                        for j in directoryStructure[i]:
                            currentDir = os.path.join(currentPath, i, j)
                            if os.path.isdir(currentDir):
                                if "language" == j:
                                    langList = os.listdir(currentDir)
                                    for lang in langList:
                                        if(os.path.isdir(os.path.join(currentDir, lang))):
                                            moduleDir = os.path.join(currentDir, lang, 'module')
                                            if not os.path.isdir(moduleDir):
                                                os.makedirs(moduleDir)
                                            if os.path.isdir(moduleDir):
                                                file = os.open(os.path.join(moduleDir, "%s.php" % moduleName), os.O_RDWR|os.O_CREAT)
                                                if file and os.write(file, getContent("%s_%s" % (i, j), moduleName)):
                                                    os.close(file)
                                                    print os.path.join(moduleDir, "%s.php" % moduleName) + " dosyası oluşturuldu."
                                                else:
                                                    print "HATA: " + os.path.join(moduleDir, "%s.php" % moduleName) + " dosyası oluşturulamadı."
                                elif "view" == j:
                                    if "catalog" == i:
                                        viewDirname = os.path.join(currentDir, 'theme', 'default', 'template', 'module')
                                    elif "admin" == i:
                                        viewDirname = os.path.join(currentDir, 'template', 'module')

                                    if not os.path.isdir(viewDirname):
                                        os.makedirs(viewDirname)
                                    if os.path.isdir(viewDirname):
                                        viewFileName = os.path.join(viewDirname, "%s.tpl" % moduleName)
                                        file = os.open(viewFileName, os.O_RDWR|os.O_CREAT)
                                        if file and os.write(file, getContent("%s_%s" % (i, j), moduleName)):
                                            os.close(file)
                                            print viewFileName + " dosyası oluşturuldu."
                                        else:
                                            print "HATA: " + viewFileName + " dosyası oluşturulamadı."
                                else:
                                    moduleDir = os.path.join(currentDir, 'module')
                                    if not os.path.exists(moduleDir):
                                        os.makedirs(moduleDir)
                                    if os.path.exists(moduleDir):
                                        file = os.open(os.path.join(moduleDir, moduleName + '.php'), os.O_RDWR|os.O_CREAT)
                                        if file and os.write(file, getContent("%s_%s" % (i, j), moduleName)):
                                            os.close(file)
                                            print os.path.join(moduleDir, moduleName + '.php') + " dosyası oluşturuldu."
                                        else:
                                            print "HATA: " + os.path.join(moduleDir, moduleName + '.php') + " dosyası olşuturulamadı."
                                    else:
                                        print "Yazma izinlerini kontrol edin"
                                        
                else:
                    print os.path.join(currentPath, i) + " dizini bulunamadı"

def main(argv, action, moduleName):
    try:
        directory = None
        opts, args = getopt.getopt(argv,"hd:",["directory=","dir=",'adminonly'])
        adminonly = False
        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit()
            elif opt in ("-d", "--dir", "--directory"):
                directory = arg
            elif opt == '--adminonly':
                adminonly = True

        if None == directory:
            directory = '.'

        if "create" == action:
            createDirectories(directory, moduleName, adminonly)
    
    except getopt.GetoptError:
        usage()
        sys.exit(2)

def usage():
    print sys.argv[0] + ' <action> <modulename> -d <directory> <options>\nActions:\n create\t\t\tCreates project build\n\nOptions:\n --adminonly\t\tCreates only admin files'


if __name__ == "__main__":
    actionList = ["create"]
    if len(sys.argv) > 2 and sys.argv[1] in actionList and len(sys.argv[2])>3: 
        main(sys.argv[3:], action=sys.argv[1], moduleName=sys.argv[2])
    else:
        usage()
        sys.exit()
