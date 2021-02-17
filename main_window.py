#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to display the main window for the BBC Football Manager program using wxPython.
This module implements the :py:class:`WxApp` and :py:class:`WxMainWindow` classes.
'''

# System libraries for the initial phase.
import sys
import os
import platform
import subprocess
import shutil
import datetime
import wx           # Try package python3-wxpython4 or python -m pip install wxPython
import wx.html2     # Try package python3-wxpython4-webview

# Application libraries.



class WxMainWindow(wx.Frame):
    '''
    :ivar int noEvents: Positive to ignore signals.
    :ivar wx.WebView browser: The WebView object to display the html on the main window.

    Class to represent the wxPython main window for the BBC Football Manager program.
    '''



    def __init__(self, game):
        '''
        :param Application application: The object that represents the formula one database application.
        :param object args: The program arguments.

        Class constructor for the :py:class:`WxMainWindow` class.
        '''
        # Initialise base classes.  The 'super' style is more modern but I prefer explicit 'wx.Frame' notation.
        # super(WxMainWindow, self).__init__(None, 1, 'Formula One Results Database')
        wx.Frame.__init__(self, None, 1, 'BBC Football Manager')

        # Report the version number.
        versionNumber = wx.version().replace('.', '·')
        print('wxPython {}.'.format(versionNumber))

        # Save the parameters.
        self.game = game

        # Intialise the application.
        self.noEvents = 0
        self.timer = None

        # Build the menu bar.
        menuBar = wx.MenuBar()
        menuFile = wx.Menu()
        menuFileExit = menuFile.Append(wx.ID_EXIT, 'Quit', 'Quit application.')
        menuBar.Append(menuFile, '&File')
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self._fileQuit, menuFileExit)

        # Build the content controlled by the sizer.
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self._webViewNavigating, self.browser)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((700, 700))

        # Display the current page.
        self.displayNextPage('')

        # Positive to ignore signals.
        self.noEvents = 0



    def _fileQuit(self, widget):
        ''' Signal handler for the 'File' → 'Quit' menu point. '''
        # Close the main window and hence exit the wxPython loop.
        self.Close()



    def _FileOpen(self, widget):
        ''' Signal handler for the 'File' → 'Open' menu point. '''
        dialogSelectFile = gtk.FileChooserDialog('Select File', None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialogSelectFile.set_default_response(gtk.RESPONSE_OK)

        oFilter = gtk.FileFilter()
        oFilter.set_name('All files')
        oFilter.add_pattern('*')
        dialogSelectFile.add_filter(oFilter)

        oFilter = gtk.FileFilter()
        oFilter.set_name('html files')
        oFilter.add_pattern('*.html')
        dialogSelectFile.add_filter(oFilter)

        response = dialogSelectFile.run()
        if response == gtk.RESPONSE_OK:
            self.application.render.html.Open(dialogSelectFile.get_filename())

        dialogSelectFile.destroy()
        self.displayCurrentPage()



    def _FileSave(self, widget):
        ''' Signal handler for the 'File' → 'Save' menu item. '''
        self.saveDocument('formulaone.html')



    def _FileSaveAs(self, widget):
        ''' Signal handler for the 'File' → 'Save As' menu item. '''
        dialogSelectFile = gtk.FileChooserDialog('Select File', None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialogSelectFile.set_default_response(gtk.RESPONSE_OK)

        oFilter = gtk.FileFilter()
        oFilter.set_name('All files')
        oFilter.add_pattern('*')
        dialogSelectFile.add_filter(oFilter)

        oFilter = gtk.FileFilter()
        oFilter.set_name('html files')
        oFilter.add_pattern('*.html')
        dialogSelectFile.add_filter(oFilter)

        response = dialogSelectFile.run()
        if response == gtk.RESPONSE_OK:
            self.saveDocument(dialogSelectFile.get_filename())

        dialogSelectFile.destroy()



    def _FilePrint(self, widget):
        ''' Signal handler for the 'File' → 'Print Preview' menu item. '''
        # Save the html to a file.
        fileName = '{}/print.html'.format(self.application.configuration.DIRECTORY)
        outFile = open(fileName, 'w')
        outFile.write(self.application.render.html.toHtml())
        outFile.close()
        if self.application.database.debug:
            print('Created \'{}\'.'.format(fileName))

        # Launch the html with the default viewer.
        subprocess.Popen(['xdg-open', fileName])



    def _ViewDebug(self, widget):
        ''' Signal handler for the 'View' -> 'Debug' menu point toggled event. '''
        self.application.database.debug = widget.get_active()
        if self.application.database.debug:
            # Add the debug stylesheet.
            self.application.render.html.stylesheets.append('file:' + os.path.dirname(os.path.realpath(__file__)) + os.sep + 'debug.css')
            for sheet in self.application.render.html.stylesheets:
                print(sheet)
        else:
            # Remove the debug stylesheet.
            if len(self.application.render.html.stylesheets) == 3:
                del self.application.render.html.stylesheets[2]
        # Update the page.
        self.OpenCurrentPage()



    def _webViewNavigating(self, event):
        ''' Signal handler for the navigating event on the wx.html2.WebView control. '''
        # print('event = {}'.format(event))
        # help(event)
        # print('event.GetTarget() = {}'.format(event.GetTarget()))
        # print('event.GetURL() = {}'.format(event.GetURL()))

        uri = event.GetURL()

        # print('Navigation Request url: ', uri)
        if uri.startswith('app:'):
            # Follow the local link.
            event.Veto()
            self.displayNextPage(uri[4:])
        # Open Links externally.
        if uri.startswith('http:') or uri.startswith('https:'):
            # Open the specified link with the default handler.  Previously this was fixed as firefox.
            event.Veto()
            subprocess.Popen(['xdg-open', uri])
        return



    def _onTimer(self, event):
        ''' Signal handler for the timer. '''
        self.timer.Stop()
        self.displayNextPage('')



    def displayNextPage(self, response):
        '''
        Display the next page on the window.
        Send the response to the game to get the next page.
        '''
        # Generate the next page from the game.
        responses = self.game.getNextPage(response)

        # Display the current page.
        self.displayCurrentPage()

        # Get ready to catch the response.
        if responses[:6] == 'delay:':
            if self.timer == None:
                self.timer = wx.Timer(self)
                self.Bind(wx.EVT_TIMER, self._onTimer, self.timer)
            delay = int(responses[7:])
            # print('delay {}'.format(delay))
            self.timer.Start(delay)





    def displayCurrentPage(self):
        '''
        Display the current content on the window.
        '''
        #if self.application.database.debug:
        #    print("displayCurrentPage()")

        # No events / signals until this finishes.
        self.noEvents += 1

        fontSize = 20;

        # Display the html content on the wx.html2.WebView control.
        html = '<html><head><style type="text/css" media="screen">body {{ font-family: Arial, Helvetica, sans-serif; font-size: {}px; }} a {{ text-decoration: none; color: inherit; }} a:hover {{ text-decoration: underline; color: inherit; }} a:visited {{ color: inherit; }} table {{ border-spacing: 0px; border-collapse: collapse; }} td {{ font-family: Arial, Helvetica, sans-serif; font-size: {}px; padding: 1px 5px 1px 5px; }} </style></head><body style="background: black; color: white;">{}</body></html>'.format(fontSize, fontSize, self.game.html)
        self.browser.SetPage(html, 'file:///')

        # Remove the wait cursor.

        # Enable events / signals again.
        self.noEvents -= 1






class WxApp(wx.App):
    '''
    :ivar WxMainWindow frame: The main window for the application.

    Class to represent the Wx application to the WxMainWindow.
    '''


    def __init__(self, game):
        '''
        Class constructor for the :py:class:`WxApp` object.
        This builds a :py:class:`WxMainWindow` object in the :py:attr:`frame` attribute.
        '''
        # Initialise the base class.
        # wx.App.__init__(self)
        super(WxApp, self).__init__()

        #self.name = 'Hello'
        #self.application = application
        #self.args = args

        # Display the main window.
        self.frame = WxMainWindow(game)
        self.frame.Show(True)

        #print('self.name = {}'.format(self.name))



    def runMainLoop(self):
        ''' Run the main wx loop. '''
        self.MainLoop()



    #def OnInit(self):
    #    ''' Class constructor. '''
    #    print('CWxApp.OnInit()')
    #    print('CWxApp.OnInit() Finished.')
    #    return True


